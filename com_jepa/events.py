"""Validate a self-contained research export; construct conservative as-of context.

This is not a production ledger, authorisation engine, or full training pipeline.
"""

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schemas/event.schema.json").read_text())
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA)
CONTEXT_TYPES = frozenset({
    "commitment.accepted", "commitment.revised", "action.recorded",
    "observation.recorded", "learning.recorded",
})


def timestamp(value):
    """The draft uses one unambiguous, second-precision UTC representation."""
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value
    ):
        raise ValueError("timestamps must use YYYY-MM-DDTHH:MM:SSZ")
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def _reject_constant(value):
    raise ValueError(f"non-finite JSON number is not allowed: {value}")


def load_events(path):
    events = []
    for line_number, line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line, parse_constant=_reject_constant))
        except ValueError as error:
            raise ValueError(f"line {line_number}: {error}") from error
    validate_events(events)
    return events


def _key(event):
    return event["organisation_id"], event["commitment_id"], event["commitment_version"]


def validate_events(events):
    """Require shapes, temporal consistency, and complete accepted-version lineage."""
    if not events:
        raise ValueError("export must contain at least one event")
    by_id = {}
    versions = {}
    initiatives = {}
    for event in events:
        errors = list(VALIDATOR.iter_errors(event))
        if errors:
            raise ValueError(f"invalid event shape: {errors[0].message}")
        event_id = event["event_id"]
        if event_id in by_id:
            raise ValueError(f"duplicate event_id: {event_id}")
        by_id[event_id] = event
        occurred = timestamp(event["occurred_at"])
        available = timestamp(event["available_at"])
        if available < occurred:
            raise ValueError(f"{event_id}: availability precedes occurrence")
        identity = _key(event)[:2]
        initiative = initiatives.setdefault(identity, event["initiative_id"])
        if initiative != event["initiative_id"]:
            raise ValueError(f"{event_id}: commitment changes initiative within export")
        if event["event_type"] in {"commitment.accepted", "commitment.revised"}:
            key = _key(event)
            if key in versions:
                raise ValueError(f"{event_id}: accepted version cannot be overwritten")
            versions[key] = event
            payload = event["payload"]
            if timestamp(payload["due_at"]) <= occurred:
                raise ValueError(f"{event_id}: accepted deadline must be in the future")
            criterion_ids = [c["criterion_id"] for c in payload["acceptance_criteria"]]
            if len(criterion_ids) != len(set(criterion_ids)):
                raise ValueError(f"{event_id}: duplicate criterion_id")

    for event in events:
        event_id, kind, payload = event["event_id"], event["event_type"], event["payload"]
        key = _key(event)
        accepted = versions.get(key)
        if accepted is None:
            raise ValueError(f"{event_id}: missing accepted commitment version")
        for clock in ("occurred_at", "available_at"):
            if timestamp(event[clock]) < timestamp(accepted[clock]):
                raise ValueError(f"{event_id}: event precedes its accepted version")
        if kind == "commitment.accepted":
            if key[2] != 1 or payload["supersedes_version"] is not None:
                raise ValueError(f"{event_id}: initial acceptance must be version 1 without predecessor")
        elif kind == "commitment.revised":
            predecessor = versions.get((*key[:2], key[2] - 1))
            if key[2] <= 1 or payload["supersedes_version"] != key[2] - 1 or predecessor is None:
                raise ValueError(f"{event_id}: broken revision lineage")
            if any(timestamp(event[c]) < timestamp(predecessor[c]) for c in ("occurred_at", "available_at")):
                raise ValueError(f"{event_id}: revision precedes predecessor")
        elif kind == "action.recorded":
            if payload["stage"] in {"authorised", "started", "completed"} and not payload["authority_ref"]:
                raise ValueError(f"{event_id}: action stage needs an authority reference")
        elif kind == "outcome.assessed":
            if payload["status"] in {"met", "not_met"}:
                if not payload["evidence_refs"]:
                    raise ValueError(f"{event_id}: settled outcome needs evidence")
                if timestamp(event["occurred_at"]) < timestamp(accepted["payload"]["due_at"]):
                    raise ValueError(f"{event_id}: settled assessment precedes version deadline")
        elif kind == "forecast.recorded":
            cutoff = timestamp(payload["as_of"])
            if not timestamp(accepted["available_at"]) <= cutoff <= timestamp(event["occurred_at"]):
                raise ValueError(f"{event_id}: forecast cutoff outside known-version/forecast interval")
            if cutoff >= timestamp(accepted["payload"]["due_at"]):
                raise ValueError(f"{event_id}: forecast cutoff must precede target deadline")
        elif kind == "learning.recorded":
            if payload["stage"] == "adopted" and not payload["authority_ref"]:
                raise ValueError(f"{event_id}: adopted learning needs an authority reference")
            if payload["stage"] == "assessed" and not payload["evidence_refs"]:
                raise ValueError(f"{event_id}: assessed learning needs evidence")
            for related_id in payload["related_event_ids"]:
                related = by_id.get(related_id)
                if related is None or related_id == event_id or related["organisation_id"] != event["organisation_id"]:
                    raise ValueError(f"{event_id}: invalid learning evidence reference")
                if timestamp(related["available_at"]) > timestamp(event["occurred_at"]):
                    raise ValueError(f"{event_id}: learning cites evidence not yet available")


def snapshot(events, as_of):
    """Select historical context only, leaving label joins and state reduction explicit.

    Sorting is deterministic for this export. Tied timestamps do not imply a causal
    event order. Forecasts and outcome assessments are always excluded in v0.1.0.
    """
    validate_events(events)
    cutoff = timestamp(as_of)
    context = [e for e in events if e["event_type"] in CONTEXT_TYPES
               and timestamp(e["occurred_at"]) <= cutoff
               and timestamp(e["available_at"]) <= cutoff]
    context.sort(key=lambda e: (e["occurred_at"], e["available_at"], e["event_id"]))
    return {"schema_version": "0.1.0", "as_of": as_of,
            "purpose": "context_only_not_a_training_dataset",
            "events": deepcopy(context)}
