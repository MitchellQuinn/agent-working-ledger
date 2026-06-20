from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from . import __version__
from .check import check_scope, format_text
from .close import CloseLedgerError, close_ledger, format_close_text
from .list import format_list_text, list_ledgers
from .new import NewLedgerError, create_ledger, format_new_text
from .supersede import SupersedeLedgerError, format_supersede_text, supersede_ledger
from .summarize import SummarizeError, format_summary_text, summarize_scope


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

    summarize_parser = subparsers.add_parser(
        "summarize",
        help="Read-only continuation summary for a working-ledger scope.",
    )
    summarize_parser.add_argument("scope", help="Path to the ledger scope to summarize.")
    summarize_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text.",
    )

    list_parser = subparsers.add_parser(
        "list",
        help="List candidate ledger scopes without adopting one.",
    )
    list_parser.add_argument(
        "--root",
        default="working-ledger",
        help="Working-ledger root directory. Defaults to working-ledger.",
    )
    list_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text.",
    )

    close_parser = subparsers.add_parser(
        "close",
        help="Close a specified ledger scope.",
    )
    close_parser.add_argument("scope", help="Path to the ledger scope to close.")
    close_parser.add_argument("--outcome", required=True, help="Closeout outcome or retrospective text.")
    close_parser.add_argument(
        "--validation-status",
        required=True,
        choices=("Not Run", "Failed", "Passed", "Partially Verified", "Stale", "Not Applicable"),
        help="Final validation status.",
    )
    close_parser.add_argument("--remaining-risks", required=True, help="Remaining risks or 'None known'.")
    close_parser.add_argument("--follow-up", required=True, help="Follow-up work or 'No follow-up needed'.")
    close_parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Defaults to text.",
    )

    supersede_parser = subparsers.add_parser(
        "supersede",
        help="Mark a specified ledger scope as superseded.",
    )
    supersede_parser.add_argument("scope", help="Path to the ledger scope to supersede.")
    supersede_parser.add_argument("--by", required=True, dest="superseded_by", help="Ledger, plan, issue, or execution path replacing this ledger.")
    supersede_parser.add_argument("--reason", required=True, help="Reason this ledger is being superseded.")
    supersede_parser.add_argument(
        "--useful",
        default="Review this ledger for potentially useful discoveries, decisions, and validation evidence.",
        help="Useful work or evidence remaining in this ledger.",
    )
    supersede_parser.add_argument("--continuation", help="Where continuation should happen. Defaults to --by.")
    supersede_parser.add_argument(
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

    if args.command == "summarize":
        try:
            result = summarize_scope(args.scope)
        except SummarizeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        if args.format == "json":
            print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
        else:
            print(format_summary_text(result))
        return 0

    if args.command == "list":
        result = list_ledgers(args.root)
        if args.format == "json":
            print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
        else:
            print(format_list_text(result))
        return 0

    if args.command == "close":
        try:
            result = close_ledger(
                args.scope,
                outcome=args.outcome,
                validation_status=args.validation_status,
                remaining_risks=args.remaining_risks,
                follow_up=args.follow_up,
            )
        except CloseLedgerError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        if args.format == "json":
            print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
        else:
            print(format_close_text(result))
        return 0

    if args.command == "supersede":
        try:
            result = supersede_ledger(
                args.scope,
                superseded_by=args.superseded_by,
                reason=args.reason,
                useful=args.useful,
                continuation=args.continuation,
            )
        except SupersedeLedgerError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        if args.format == "json":
            print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
        else:
            print(format_supersede_text(result))
        return 0

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
