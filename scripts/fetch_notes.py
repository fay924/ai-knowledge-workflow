#!/usr/bin/env python3
"""Fetch Get笔记 smart content without exposing credentials."""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from state import ingest_notes, read_seen


BASE_URL = "https://openapi.biji.com"
CONFIG_FILE = Path(os.environ.get("CAPTURE_CONFIG_DIR", Path.home() / ".config" / "capture-to-notion")) / "config.json"
AUDIO_TYPES = {"audio", "meeting", "local_audio", "recorder_audio", "internal_record"}


def credentials():
    try:
        config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}
    section = config.get("getnote", {})
    return (
        os.environ.get("GETNOTE_API_KEY") or section.get("api_key", ""),
        os.environ.get("GETNOTE_CLIENT_ID") or section.get("client_id", ""),
    )


def safe_parse(text):
    safe = re.sub(r'"(id|note_id|next_cursor|parent_id|follow_id|live_id)"\s*:\s*(\d+)', r'"\1":"\2"', text)
    return json.loads(safe)


def api_get(path):
    api_key, client_id = credentials()
    if not api_key or not client_id:
        raise RuntimeError("Get笔记尚未配置。先运行 python3 scripts/setup.py set-getnote")
    request = urllib.request.Request(f"{BASE_URL}{path}")
    request.add_header("Authorization", api_key)
    request.add_header("X-Client-ID", client_id)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return safe_parse(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Get笔记请求失败：HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError("Get笔记请求失败：请检查网络或稍后重试") from exc


def fetch_detail(note_id):
    data = api_get(f"/open/api/v1/resource/note/detail?id={note_id}")
    return data.get("data", {}).get("note", {})


def parse_datetime(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.astimezone()


def smart_content(note):
    return (note.get("content") or "").strip()


def source_url(note):
    value = note.get("web_page") or {}
    return value.get("url", "") if isinstance(value, dict) else ""


def entry(note, preview_chars=None):
    content = smart_content(note)
    value = {
        "id": str(note.get("id") or note.get("note_id") or ""),
        "title": (note.get("title") or content[:60].replace("\n", " ")).strip(),
        "type": note.get("note_type", "?"),
        "created_at": note.get("created_at", "?"),
        "content_source": "getnote.content",
        "original_content_read": False,
    }
    if preview_chars is None:
        value["content"] = content
    else:
        value["content_preview"] = content[:preview_chars]
        value["content_length"] = len(content)
        value["preview_truncated"] = len(content) > preview_chars
    url = source_url(note)
    if url:
        value["source_url"] = url
    return value


def fetch_list(since_date, max_pages):
    notes = []
    cursor = 0
    for _ in range(max_pages):
        data = api_get(f"/open/api/v1/resource/note/list?since_id={cursor}").get("data", {})
        batch = data.get("notes") or []
        if not batch:
            break
        notes.extend(batch)
        if not data.get("has_more") or not data.get("next_cursor"):
            break
        cursor = data["next_cursor"]
    if not since_date:
        return notes
    threshold = parse_datetime(since_date)
    return [note for note in notes if note.get("created_at") and parse_datetime(note["created_at"]) > threshold]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--detail", metavar="NOTE_ID")
    parser.add_argument("--preview-chars", type=int, default=1200)
    parser.add_argument("--record-seen", action="store_true")
    parser.add_argument("--max-pages", type=int, default=5)
    args = parser.parse_args()
    try:
        if args.detail:
            print(json.dumps(entry(fetch_detail(args.detail)), ensure_ascii=False, indent=2))
            return
        since = read_seen()
        notes = fetch_list(since, args.max_pages)
        results = []
        for note in notes:
            if note.get("note_type") in AUDIO_TYPES:
                try:
                    note = fetch_detail(str(note.get("id"))) or note
                except RuntimeError:
                    pass
            results.append(entry(note, args.preview_chars))
        latest = results[0].get("created_at") if results else since
        output = {"since": since or "beginning", "count": len(results), "mode": "preview", "notes": results}
        if args.record_seen:
            output["queue"] = ingest_notes(results, latest)
        print(json.dumps(output, ensure_ascii=False, indent=2))
    except RuntimeError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

