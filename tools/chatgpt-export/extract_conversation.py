#!/usr/bin/env python3
"""Convert a ChatGPT conversation JSON file into a readable Markdown file.

Accepts either:
  * a full account export (conversations.json: a list of conversations), or
  * a single conversation object (mapping / current_node), as returned by
    /backend-api/conversation/<id>.

Usage:
  python -I -X utf8 extract_conversation.py input.json -o output.md
  python -I -X utf8 extract_conversation.py input.json --list
  python -I -X utf8 extract_conversation.py input.json --id <id> -o output.md
  python -I -X utf8 extract_conversation.py input.json --title "keyword" -o output.md
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_conversations(obj):
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        if isinstance(obj.get("conversations"), list):
            return obj["conversations"]
        if isinstance(obj.get("mapping"), dict):
            return [obj]
        if isinstance(obj.get("conversation"), dict):
            return [obj["conversation"]]
    return []


def message_text(message):
    if not isinstance(message, dict):
        return ""
    content = message.get("content") or {}
    parts = content.get("parts")
    chunks = []

    if isinstance(parts, list):
        for part in parts:
            if isinstance(part, str):
                chunks.append(part)
            elif isinstance(part, dict):
                text = part.get("text")
                if isinstance(text, str) and text:
                    chunks.append(text)

    if not chunks and isinstance(content.get("text"), str):
        chunks.append(content["text"])

    return "\n".join(chunks).strip()


def conversation_nodes(conversation):
    mapping = conversation.get("mapping") or {}
    current = conversation.get("current_node")

    if current and current in mapping:
        nodes = []
        seen = set()
        while current and current in mapping and current not in seen:
            seen.add(current)
            node = mapping[current]
            nodes.append(node)
            current = node.get("parent")
        nodes.reverse()
        return nodes

    nodes = [node for node in mapping.values() if isinstance(node, dict) and node.get("message")]
    nodes.sort(key=lambda node: (node.get("message") or {}).get("create_time") or 0)
    return nodes


def format_time(value):
    if not isinstance(value, (int, float)):
        return None
    try:
        return datetime.fromtimestamp(value, tz=timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )
    except (OverflowError, OSError, ValueError):
        return None


def render(conversation, source_url=None):
    title = conversation.get("title") or "ChatGPT conversation"
    conversation_id = conversation.get("id")
    created = format_time(conversation.get("create_time"))
    extracted = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    sections = []
    count = 0
    for node in conversation_nodes(conversation):
        message = node.get("message")
        if not isinstance(message, dict):
            continue
        role = (message.get("author") or {}).get("role") or "unknown"
        text = message_text(message)
        if not text:
            continue
        count += 1
        stamp = format_time(message.get("create_time"))
        heading = f"## {count} · {role}"
        if stamp:
            heading += f" · {stamp}"
        sections.append(f"{heading}\n\n{text}\n")

    header = [f"# {title}", ""]
    if conversation_id:
        header.append(f"- id: `{conversation_id}`")
    if created:
        header.append(f"- created: {created}")
    if source_url:
        header.append(f"- source: {source_url}")
    header.append(f"- extracted: {extracted}")
    header.append(f"- messages: {count}")
    header.append("")

    return "\n".join(header) + "\n" + "\n".join(sections), count


def main():
    parser = argparse.ArgumentParser(description="Extract ChatGPT conversation JSON to Markdown.")
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("chatgpt-export.md"))
    parser.add_argument("--id", help="select a conversation by id")
    parser.add_argument("--title", help="select a conversation by title substring")
    parser.add_argument("--source-url", help="source URL to record in the header")
    parser.add_argument("--list", action="store_true", help="list conversations and exit")
    args = parser.parse_args()

    conversations = find_conversations(load_json(args.input))
    if not conversations:
        sys.exit(
            "No conversation found. Expected a full export list or a single "
            "conversation object with a mapping."
        )

    if args.list:
        for index, conversation in enumerate(conversations):
            print(f"{index}\t{conversation.get('id', '?')}\t{conversation.get('title', '')}")
        return

    if args.id:
        conversations = [c for c in conversations if c.get("id") == args.id]
    elif args.title:
        needle = args.title.lower()
        conversations = [
            c for c in conversations if needle in (c.get("title") or "").lower()
        ]

    if len(conversations) != 1:
        print(
            f"{len(conversations)} matching conversations. "
            "Use --list and then --id to select exactly one.",
            file=sys.stderr,
        )
        for conversation in conversations[:50]:
            print(
                f"  {conversation.get('id', '?')}\t{conversation.get('title', '')}",
                file=sys.stderr,
            )
        sys.exit(2)

    markdown, count = render(conversations[0], source_url=args.source_url)
    args.output.write_text(markdown, encoding="utf-8")
    print(f"wrote {args.output} ({count} messages, {len(markdown)} chars)")


if __name__ == "__main__":
    main()
