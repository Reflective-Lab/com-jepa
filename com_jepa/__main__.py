"""Run from a source checkout: python -m com_jepa validate|snapshot ..."""

import argparse
import json

from .events import load_events, snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="validate a self-contained JSONL export")
    validate.add_argument("path")
    project = commands.add_parser("snapshot", help="emit only context available at a cutoff")
    project.add_argument("path")
    project.add_argument("--as-of", required=True)
    args = parser.parse_args()
    try:
        events = load_events(args.path)
        if args.command == "validate":
            print(f"Validated {len(events)} events against draft 0.1.0 and semantic checks.")
        else:
            print(json.dumps(snapshot(events, args.as_of), indent=2))
    except (ValueError, OSError) as error:
        parser.exit(1, f"error: {error}\n")


if __name__ == "__main__":
    main()
