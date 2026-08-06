#!/usr/bin/env python3
"""Local setup helper. Secrets never print or enter repository files."""

import argparse
import getpass
import json
import os
import stat
import sys
from pathlib import Path


CONFIG_DIR = Path(
    os.environ.get(
        "AI_KNOWLEDGE_CONFIG_DIR",
        os.environ.get("CAPTURE_CONFIG_DIR", Path.home() / ".config" / "ai-knowledge-workflow"),
    )
)
CONFIG_FILE = CONFIG_DIR / "config.json"
ECHO_SCRIPT = Path(__file__).with_name("echo_state.py")


def load_config():
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_config(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    CONFIG_FILE.chmod(stat.S_IRUSR | stat.S_IWUSR)


def masked(value):
    return "configured" if value else "missing"


def status():
    data = load_config()
    notion = data.get("notion", {})
    getnote = data.get("getnote", {})
    mapping = notion.get("mapping", {})
    getnote_credentials = bool(
        (getnote.get("api_key") or os.environ.get("GETNOTE_API_KEY"))
        and (getnote.get("client_id") or os.environ.get("GETNOTE_CLIENT_ID"))
    )
    result = {
        "getnote_access": masked(getnote.get("connector") or getnote_credentials),
        "notion_access": masked(notion.get("token") or os.environ.get("NOTION_TOKEN") or notion.get("connector")),
        "notion_root_page": masked(notion.get("root_page_id")),
        "notion_database_map": "configured" if all(mapping.get(k) for k in ("notes", "projects", "areas", "resources")) else "missing",
        "daily_echo_module": "bundled" if ECHO_SCRIPT.exists() else "missing",
        "config_file": str(CONFIG_FILE),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def set_getnote():
    data = load_config()
    section = data.setdefault("getnote", {})
    section["api_key"] = getpass.getpass("Get笔记 API Key（输入不可见）: ").strip()
    section["client_id"] = getpass.getpass("Get笔记 Client ID（输入不可见）: ").strip()
    if not section["api_key"] or not section["client_id"]:
        raise ValueError("API Key 和 Client ID 都不能为空")
    save_config(data)
    print("Get笔记凭证已保存到本机。")


def set_notion_token():
    data = load_config()
    token = getpass.getpass("Notion Token（输入不可见）: ").strip()
    if not token:
        raise ValueError("Notion Token 不能为空")
    data.setdefault("notion", {})["token"] = token
    save_config(data)
    print("Notion Token 已保存到本机。")


def set_notion_connector():
    data = load_config()
    data.setdefault("notion", {})["connector"] = True
    save_config(data)
    print("已记录使用宿主 AI 的 Notion 连接器；仍需由 AI 实际读取根页面并验证权限。")


def set_getnote_connector():
    data = load_config()
    data.setdefault("getnote", {})["connector"] = True
    save_config(data)
    print("已记录使用宿主 AI 的得到大脑连接器；仍需由 AI 实际读取最近一条笔记验证权限。")


def set_notion_map(args):
    data = load_config()
    notion = data.setdefault("notion", {})
    notion["root_page_id"] = args.root_page
    notion["mapping"] = {
        "notes": args.notes,
        "projects": args.projects,
        "areas": args.areas,
        "resources": args.resources,
    }
    save_config(data)
    print("Notion 数据库映射已保存。")


def verify():
    result = status()
    missing = [key for key, value in result.items() if key != "config_file" and value == "missing"]
    if missing:
        print(json.dumps({"ok": False, "missing": missing}, ensure_ascii=False))
        return 1
    print(json.dumps({"ok": True}, ensure_ascii=False))
    return 0


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("verify")
    sub.add_parser("set-getnote")
    sub.add_parser("set-notion-token")
    sub.add_parser("set-notion-connector")
    sub.add_parser("set-getnote-connector")
    notion_map = sub.add_parser("set-notion-map")
    notion_map.add_argument("--root-page", required=True)
    notion_map.add_argument("--notes", required=True)
    notion_map.add_argument("--projects", required=True)
    notion_map.add_argument("--areas", required=True)
    notion_map.add_argument("--resources", required=True)
    args = parser.parse_args()

    try:
        if args.command == "status":
            status()
        elif args.command == "verify":
            sys.exit(verify())
        elif args.command == "set-getnote":
            set_getnote()
        elif args.command == "set-notion-token":
            set_notion_token()
        elif args.command == "set-notion-connector":
            set_notion_connector()
        elif args.command == "set-getnote-connector":
            set_getnote_connector()
        elif args.command == "set-notion-map":
            set_notion_map(args)
    except (OSError, ValueError) as exc:
        print(f"配置失败：{exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
