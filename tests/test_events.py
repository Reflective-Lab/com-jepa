from copy import deepcopy
from pathlib import Path
import unittest

from com_jepa.events import load_events, snapshot, timestamp, validate_events


FIXTURE = Path(__file__).resolve().parent.parent / "examples/fictional-trajectory.jsonl"


class EventContractTests(unittest.TestCase):
    def setUp(self):
        self.events = load_events(FIXTURE)

    def test_late_evidence_and_future_actions_are_excluded(self):
        result = snapshot(self.events, "2026-01-06T12:00:00Z")
        self.assertEqual([e["event_id"] for e in result["events"]], ["e01", "e02", "e03"])

    def test_context_always_excludes_forecasts_and_outcome_assessments(self):
        result = snapshot(self.events, "2026-02-01T00:00:00Z")
        self.assertFalse({"forecast.recorded", "outcome.assessed"} &
                         {e["event_type"] for e in result["events"]})

    def test_revision_preserves_both_promises_and_original_outcome(self):
        result = snapshot(self.events, "2026-01-08T12:00:00Z")
        promises = [e for e in result["events"] if e["event_type"].startswith("commitment.")]
        self.assertEqual([e["commitment_version"] for e in promises], [1, 2])
        self.assertEqual([e["payload"]["due_at"] for e in promises],
                         ["2026-01-09T17:00:00Z", "2026-01-12T17:00:00Z"])
        outcomes = [e for e in self.events if e["event_type"] == "outcome.assessed"]
        self.assertEqual([(e["commitment_version"], e["payload"]["status"]) for e in outcomes],
                         [(1, "not_met"), (2, "met")])

    def test_cutoff_includes_exact_available_time_and_empty_past(self):
        self.assertEqual(snapshot(self.events, "2026-01-01T00:00:00Z")["events"], [])
        ids = [e["event_id"] for e in snapshot(self.events, "2026-01-07T09:00:00Z")["events"]]
        self.assertIn("e04", ids)
        self.assertNotIn("e06", ids)

    def test_replay_is_input_order_independent_and_does_not_mutate_source(self):
        cutoff = "2026-01-08T12:00:00Z"
        original = deepcopy(self.events)
        result = snapshot(self.events, cutoff)
        self.assertEqual(result, snapshot(list(reversed(self.events)), cutoff))
        result["events"][0]["payload"]["intent"] = "changed"
        self.assertEqual(self.events, original)

    def test_duplicate_event_or_accepted_version_is_rejected(self):
        for change_id in (False, True):
            with self.subTest(change_id=change_id):
                duplicate = deepcopy(self.events[0])
                if change_id:
                    duplicate["event_id"] = "another-acceptance"
                with self.assertRaises(ValueError):
                    validate_events(self.events + [duplicate])

    def test_missing_or_broken_version_lineage_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing accepted|broken revision"):
            validate_events([e for e in self.events if e["commitment_version"] == 2])
        self.events[6]["payload"]["supersedes_version"] = 2
        with self.assertRaisesRegex(ValueError, "broken revision"):
            validate_events(self.events)

    def test_unknown_censored_and_disputed_are_not_binary_labels(self):
        for status in ("unknown", "right_censored", "disputed"):
            with self.subTest(status=status):
                events = deepcopy(self.events)
                events[7]["payload"]["status"] = status
                events[7]["payload"]["evidence_refs"] = []
                validate_events(events)
                self.assertEqual(events[7]["payload"]["status"], status)

    def test_settled_outcome_requires_evidence_and_deadline_passage(self):
        for field, value in (("evidence_refs", []), ("occurred_at", "2026-01-09T16:00:00Z")):
            events = deepcopy(self.events)
            if field == "occurred_at":
                events[7][field] = value
            else:
                events[7]["payload"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_events(events)

    def test_invalid_clock_and_availability_order_are_rejected(self):
        for value in ("2026-02-30T00:00:00Z", "2026-01-01", "2026-01-01T00:00:00+01:00"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                timestamp(value)
        self.events[1]["available_at"] = "2026-01-06T09:59:00Z"
        with self.assertRaisesRegex(ValueError, "availability precedes"):
            validate_events(self.events)

    def test_forecast_cannot_claim_context_from_after_it_was_made(self):
        self.events[4]["payload"]["as_of"] = "2026-01-07T12:00:00Z"
        with self.assertRaisesRegex(ValueError, "forecast cutoff"):
            validate_events(self.events)

    def test_authorised_action_needs_authority(self):
        self.events[5]["payload"]["authority_ref"] = None
        with self.assertRaisesRegex(ValueError, "authority reference"):
            validate_events(self.events)

    def test_learning_cannot_cite_future_evidence(self):
        self.events[10]["occurred_at"] = "2026-01-08T12:00:00Z"
        with self.assertRaisesRegex(ValueError, "not yet available"):
            validate_events(self.events)

    def test_undefined_payload_fields_and_empty_export_are_rejected(self):
        self.events[2]["payload"]["private_transcript"] = "unexpected"
        with self.assertRaisesRegex(ValueError, "invalid event shape"):
            validate_events(self.events)
        with self.assertRaisesRegex(ValueError, "at least one"):
            validate_events([])


if __name__ == "__main__":
    unittest.main()
