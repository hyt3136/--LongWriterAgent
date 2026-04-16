"""Draft writer for chapter-8 loop."""

from __future__ import annotations

from typing import Dict


def write_draft(chapter_title: str, context: Dict) -> Dict:
    context_summary = " | ".join(chunk.get("text", "")[:40] for chunk in context.get("chunks", [])[:3])
    content = f"章节：{chapter_title}\n基于上下文：{context_summary}\n正文草稿：主线推进。"
    return {"title": chapter_title, "content": content}
