"""Draft reviser."""

from __future__ import annotations

from typing import Dict


def revise_draft(draft: Dict, review: Dict, round_index: int) -> Dict:
    content = str(draft.get("content", ""))
    suffix = f"\n修订轮次{round_index}：补充冲突、动机与转折。"
    return {"title": draft.get("title", ""), "content": content + suffix}
