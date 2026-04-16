"""Context assembler with token-like budget controls."""

from __future__ import annotations

from typing import Dict, List


def assemble_context(retrieved: List[Dict], recent: List[Dict], max_chars: int = 800) -> Dict:
    chunks = []
    used = 0

    # Recent chapters first to preserve narrative continuity.
    for item in recent:
        text = str(item.get("summary", ""))
        if not text:
            continue
        if used + len(text) > max_chars:
            break
        chunks.append({"kind": "recent", "text": text})
        used += len(text)

    for item in retrieved:
        text = str(item.get("text", ""))
        if not text:
            continue
        if used + len(text) > max_chars:
            break
        chunks.append({"kind": "retrieved", "text": text, "score": item.get("score", 0)})
        used += len(text)

    return {"chunks": chunks, "used_chars": used, "max_chars": max_chars}
