#!/usr/bin/env python3
"""Convert a ChatGPT conversation JSON file into a readable Markdown file.

Accepts either:
  * a full account export (conversations.json: a list of conversations), or
  * a single conversation object (mapping / current_node), as returned by
    /backend-api/conversation/<id> or /backend-api/share/<share_id>.

Modes:
  text  (default) user and assistant text only, plus reasoning recaps
  full  text plus code-interpreter calls and execution outputs

Usage:
  python -I -X utf8 extract_conversation.py input.json -o output.md
  python -I -X utf8 extract_conversation.py input.json --mode full -o all.md
  python -I -X utf8 extract_conversation.py input.json --list
  python -I -X utf8 extract_conversation.py input.json --id <id> -o output.md
  python -I -X utf8 extract_conversation.py input.json --title "keyword" -o output.md
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REDACTED = "The output of this plugin was redacted."


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


def is_hidden(message):
    metadata = message.get("metadata") or {}
    return bool(metadata.get("is_visually_hidden_from_conversation"))


def message_payload(message):
    """Return (kind, text, language) for a message, or None to skip it."""
    if not isinstance(message, dict):
        return None

    content = message.get("content") or {}
    content_type = content.get("content_type")
    parts = content.get("parts")

    if content_type == "text":
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
        text = "\n".join(chunks).strip()
        if not text or text == REDACTED:
            return None
        return ("text", text, "")

    if content_type == "code":
        text = content.get("text")
        if isinstance(text, str) and text.strip():
            return ("code", text.strip(), content.get("language") or "")
        return None

    if content_type == "execution_output":
        text = content.get("text")
        if isinstance(text, str) and text.strip() and text.strip() != REDACTED:
            return ("output", text.strip(), "")
        return None

    if content_type == "reasoning_recap":
        text = content.get("content")
        if isinstance(text, str) and text.strip():
            return ("recap", text.strip(), "")
        return None

    return None


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


def fence(text, language=""):
    ticks = "````"
    while ticks in text:
        ticks += "`"
    return f"{ticks}{language}\n{text}\n{ticks}"


def render(conversation, source_url=None, mode="text", include_hidden=False):
    title = conversation.get("title") or "ChatGPT conversation"
    conversation_id = conversation.get("id") or conversation.get("conversation_id")
    created = format_time(conversation.get("create_time"))
    extracted = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    sections = []
    count = 0
    times = []
    for node in conversation_nodes(conversation):
        message = node.get("message")
        if not isinstance(message, dict):
            continue
        if not include_hidden and is_hidden(message):
            continue

        role = (message.get("author") or {}).get("role") or "unknown"
        payload = message_payload(message)
        if payload is None:
            continue

        kind, text, language = payload
        if mode == "text" and kind not in ("text", "recap"):
            continue

        count += 1
        created_time = message.get("create_time")
        if isinstance(created_time, (int, float)):
            times.append(created_time)
        stamp = format_time(created_time)
        heading = f"## {count} · {role}"
        if kind == "code":
            heading += f" · code ({language})" if language else " · code"
        elif kind == "output":
            heading += " · output"
        elif kind == "recap":
            heading += " · recap"
        if stamp:
            heading += f" · {stamp}"

        if kind == "code":
            body = fence(text, language)
        elif kind == "output":
            body = fence(text, "text")
        elif kind == "recap":
            body = f"_{text}_"
        else:
            body = text

        sections.append(f"{heading}\n\n{body}\n")

    header = [f"# {title}", ""]
    if conversation_id:
        header.append(f"- id: `{conversation_id}`")
    if created:
        header.append(f"- record created: {created}")
    if times:
        header.append(f"- time range: {format_time(min(times))} -> {format_time(max(times))}")
    if source_url:
        header.append(f"- source: {source_url}")
    header.append(f"- extracted: {extracted}")
    header.append(f"- mode: {mode}")
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
    parser.add_argument("--mode", choices=("text", "full"), default="text")
    parser.add_argument("--include-hidden", action="store_true")
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

    markdown, count = render(
        conversations[0],
        source_url=args.source_url,
        mode=args.mode,
        include_hidden=args.include_hidden,
    )
    args.output.write_text(markdown, encoding="utf-8")
    print(f"wrote {args.output} ({count} messages, {len(markdown)} chars)")


if __name__ == "__main__":
    main()
