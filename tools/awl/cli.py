from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from . import __version__
from .check import check_scope, format_text
from .new import NewLedgerError, create_ledger, format_new_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="awl",
        description="Agent Working Ledger helper tooling.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)
    check_parser = subparsers.add_parser(
        "check",
        help="Read-only validation for a working-ledger scope.",
    )
    check_parser.add_argument("scope", help="Path to the ledger scope to check.")
    check_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text.",
    )

    new_parser = subparsers.add_parser(
        "new",
        help="Create a new working-ledger scope.",
    )
    new_parser.add_argument("title", help="Task title.")
    new_parser.add_argument(
        "--root",
        default="working-ledger",
        help="Ledger root directory. Defaults to working-ledger.",
    )
    new_parser.add_argument("--slug", help="Optional task slug appended to generated owner IDs.")
    new_parser.add_argument("--owner-id", help="Explicit owner ID. Refuses to overwrite existing scopes.")
    new_parser.add_argument(
        "--owner-source",
        choices=("session-id", "generated-id", "user-assigned", "wrapper-assigned"),
        help="Owner source. Defaults to generated-id or user-assigned based on owner ID generation.",
    )
    new_parser.add_argument(
        "--runtime",
        default="generic-agent",
        help="Agent runtime name recorded in OWNER.md and ledger.md. Defaults to generic-agent.",
    )
    new_parser.add_argument(
        "--created-by",
        default="awl",
        help="Creator recorded in OWNER.md. Defaults to awl.",
    )
    new_parser.add_argument("--objective", help="User objective. Defaults to the task title.")
    new_parser.add_argument(
        "--related",
        default="Not Applicable",
        help="Related branch, issue, plan, or ledger. Defaults to Not Applicable.",
    )
    new_parser.add_argument("--handoff", action="store_true", help="Also create handoff.md.")
    new_parser.add_argument("--machine-state", action="store_true", help="Also create machine-state.json.")
    new_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "check":
        result = check_scope(args.scope)
        if args.format == "json":
            print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
        else:
            print(format_text(result))
        return 0 if result.ok else 1

    if args.command == "new":
        try:
            result = create_ledger(
                args.title,
                root=args.root,
                slug=args.slug,
                owner_id=args.owner_id,
                owner_source=args.owner_source,
                runtime=args.runtime,
                created_by=args.created_by,
                objective=args.objective,
                related=args.related,
                handoff=args.handoff,
                machine_state=args.machine_state,
            )
        except NewLedgerError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

        if args.format == "json":
            print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
        else:
            print(format_new_text(result))
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
