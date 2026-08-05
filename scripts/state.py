#!/usr/bin/env python3
"""Manage retrieval and write checkpoints without storing credentials."""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


CONFIG_DIR = Path(os.environ.get("CAPTURE_CONFIG_DIR", Path.home() / ".config" / "capture-to-notion"))
STATE_FILE = CONFIG_DIR / "state.json"
FINAL_STATUSES = {"written", "skipped"}
VALID_STATUSES = {"new", "shown", "confirmed", "written", "skipped"}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = utc_now()
    STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    STATE_FILE.chmod(0o600)


def read_checkpoint():
    return load_state().get("last_capture")


def read_seen():
    state = load_state()
    return state.get("last_seen") or state.get("last_capture")


def set_baseline(timestamp=None):
    """Start future retrieval at now, without treating older notes as processed."""
    state = load_state()
    state["last_seen"] = timestamp or utc_now()
    state.setdefault("pending_notes", {})
    save_state(state)
    return state["last_seen"]


def ingest_notes(notes, last_seen=None):
    state = load_state()
    queue = state.setdefault("pending_notes", {})
    now = utc_now()
    added = 0
    for note in notes:
        note_id = str(note.get("id", ""))
        if not note_id:
            continue
        item = queue.get(note_id) or {"status": "new", "first_seen_at": now}
        if note_id not in queue:
            added += 1
        for field in ("title", "type", "created_at", "tags", "content_preview", "content_length", "preview_truncated", "headings", "source_url"):
            if field in note:
                item[field] = note[field]
        item["last_retrieved_at"] = now
        queue[note_id] = item
    if last_seen:
        state["last_seen"] = last_seen
    save_state(state)
    return {"added": added, "queued": len(queue), "last_seen": state.get("last_seen")}


def mark_notes(note_ids, status):
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid status: {status}")
    state = load_state()
    queue = state.setdefault("pending_notes", {})
    now = utc_now()
    changed = []
    for note_id in note_ids:
        if note_id in queue:
            queue[note_id]["status"] = status
            queue[note_id][f"{status}_at"] = now
            changed.append(note_id)
    save_state(state)
    return changed


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "seen":
        print(read_seen() or "NONE")
    elif command == "baseline":
        print(set_baseline(sys.argv[2] if len(sys.argv) > 2 else None))
    elif command == "mark" and len(sys.argv) >= 4:
        print(json.dumps(mark_notes(sys.argv[3:], sys.argv[2]), ensure_ascii=False))
    else:
        print(f"Usage: {sys.argv[0]} seen|baseline [timestamp]|mark STATUS ID...", file=sys.stderr)
        sys.exit(1)
