#!/usr/bin/env python3
"""Manage Daily Echo scans and user-confirmed proposals."""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


CONFIG_DIR = Path(
    os.environ.get(
        "AI_KNOWLEDGE_CONFIG_DIR",
        os.environ.get("CAPTURE_CONFIG_DIR", Path.home() / ".config" / "ai-knowledge-workflow"),
    )
)
STATE_FILE = Path(os.environ.get("DAILY_ECHO_STATE_FILE", CONFIG_DIR / "echo-state.json"))
RESULT_STATUSES = {"collision_found", "no_collision", "error"}
PROPOSAL_STATUSES = {"proposed", "confirmed", "dismissed", "applied"}
PROPOSAL_ACTIONS = {
    "append_note",
    "link_existing",
    "create_note",
    "create_task",
    "create_project",
    "create_idea",
    "update_ai_experiment",
    "change_priority",
}


def now_iso():
    return datetime.now().astimezone().isoformat()


def load_state():
    try:
        value = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = now_iso()
    temporary = STATE_FILE.with_suffix(STATE_FILE.suffix + ".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.chmod(0o600)
    os.replace(temporary, STATE_FILE)
    STATE_FILE.chmod(0o600)


def enqueue(args):
    state = load_state()
    records = state.setdefault("notes", {})
    existing = records.get(args.note_id)
    if existing and existing.get("status") in {"collision_found", "no_collision"} and not args.force:
        return {"enqueued": False, "reason": "already_scanned", "record": existing}

    timestamp = now_iso()
    record = existing or {"note_id": args.note_id, "first_queued_at": timestamp}
    notion_page_ids = list(dict.fromkeys(args.notion_page_id))
    record.update({
        "notion_page_id": notion_page_ids[0],
        "notion_page_ids": notion_page_ids,
        "title": args.title,
        "source": args.source,
        "written_at": args.written_at or record.get("written_at") or timestamp,
        "queued_at": timestamp,
        "status": "queued",
    })
    if args.force:
        record["force_rescan_at"] = timestamp
    records[args.note_id] = record
    save_state(state)
    return {"enqueued": True, "record": record}


def pending():
    records = load_state().get("notes", {})
    rows = [record for record in records.values() if record.get("status") in {"queued", "error"}]
    return sorted(rows, key=lambda row: row.get("queued_at", ""))


def mark(args):
    state = load_state()
    records = state.setdefault("notes", {})
    if args.note_id not in records:
        raise KeyError(f"unknown note ID: {args.note_id}")
    record = records[args.note_id]
    record.update({
        "status": args.status,
        "scanned_at": now_iso(),
        "matched_page_ids": list(dict.fromkeys(args.match or [])),
        "collision_count": len(set(args.match or [])),
        "summary": args.summary or "",
    })
    save_state(state)
    return record


def mark_shown(args):
    state = load_state()
    records = state.setdefault("notes", {})
    timestamp = now_iso()
    changed = []
    for note_id in args.note_ids:
        if note_id in records:
            records[note_id]["displayed_at"] = timestamp
            changed.append(note_id)
    save_state(state)
    return changed


def propose(args):
    state = load_state()
    proposals = state.setdefault("proposals", {})
    existing = proposals.get(args.proposal_id)
    if existing and not args.force:
        return {"created": False, "reason": "already_exists", "proposal": existing}
    timestamp = now_iso()
    proposal = existing or {"proposal_id": args.proposal_id, "created_at": timestamp}
    proposal.update({
        "status": "proposed",
        "action": args.action,
        "source_note_ids": list(dict.fromkeys(args.source_note_id)),
        "target_page_ids": list(dict.fromkeys(args.target_page_id or [])),
        "summary": args.summary,
        "updated_at": timestamp,
    })
    proposals[args.proposal_id] = proposal
    save_state(state)
    return {"created": existing is None, "proposal": proposal}


def list_proposals(statuses=None):
    wanted = set(statuses or [])
    rows = [
        proposal
        for proposal in load_state().get("proposals", {}).values()
        if not wanted or proposal.get("status") in wanted
    ]
    return sorted(rows, key=lambda row: row.get("created_at", ""))


def decide(args):
    state = load_state()
    proposals = state.setdefault("proposals", {})
    if args.proposal_id not in proposals:
        raise KeyError(f"unknown proposal ID: {args.proposal_id}")
    proposal = proposals[args.proposal_id]
    timestamp = now_iso()
    proposal["status"] = args.status
    proposal[f"{args.status}_at"] = timestamp
    proposal["updated_at"] = timestamp
    if args.note:
        proposal["decision_note"] = args.note
    save_state(state)
    return proposal


def stats():
    counts = {}
    for record in load_state().get("notes", {}).values():
        status = record.get("status", "queued")
        counts[status] = counts.get(status, 0) + 1
    return counts


def build_parser():
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    add = commands.add_parser("enqueue")
    add.add_argument("--note-id", required=True)
    add.add_argument("--notion-page-id", required=True, action="append")
    add.add_argument("--title", required=True)
    add.add_argument("--source", default="getnote")
    add.add_argument("--written-at")
    add.add_argument("--force", action="store_true")

    commands.add_parser("pending")

    update = commands.add_parser("mark")
    update.add_argument("note_id")
    update.add_argument("status", choices=sorted(RESULT_STATUSES))
    update.add_argument("--match", action="append")
    update.add_argument("--summary")

    shown = commands.add_parser("mark-shown")
    shown.add_argument("note_ids", nargs="+")

    proposal = commands.add_parser("propose")
    proposal.add_argument("--proposal-id", required=True)
    proposal.add_argument("--source-note-id", required=True, action="append")
    proposal.add_argument("--action", required=True, choices=sorted(PROPOSAL_ACTIONS))
    proposal.add_argument("--target-page-id", action="append")
    proposal.add_argument("--summary", required=True)
    proposal.add_argument("--force", action="store_true")

    proposal_list = commands.add_parser("proposals")
    proposal_list.add_argument("statuses", nargs="*", choices=sorted(PROPOSAL_STATUSES))

    decision = commands.add_parser("decide")
    decision.add_argument("proposal_id")
    decision.add_argument("status", choices=sorted(PROPOSAL_STATUSES - {"proposed"}))
    decision.add_argument("--note")

    commands.add_parser("stats")
    return root


def main():
    args = build_parser().parse_args()
    if args.command == "enqueue":
        result = enqueue(args)
    elif args.command == "pending":
        result = pending()
    elif args.command == "mark":
        result = mark(args)
    elif args.command == "mark-shown":
        result = mark_shown(args)
    elif args.command == "propose":
        result = propose(args)
    elif args.command == "proposals":
        result = list_proposals(args.statuses)
    elif args.command == "decide":
        result = decide(args)
    else:
        result = stats()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
