"""Quality reviewer with deterministic scoring."""

from __future__ import annotations

from typing import Dict


def review_draft(draft: Dict) -> Dict:
    content = str(draft.get("content", ""))
    length_score = 8 if len(content) > 40 else 5
    repetition_score = 6 if content.count("主线") > 2 else 8
    total = round((length_score + repetition_score) / 2, 2)
    passed = total >= 7.0
    issues = [] if passed else ["内容长度不足或重复度偏高"]
    return {
        "total_score": total,
        "passed": passed,
        "issues": issues,
        "suggestions": [] if passed else ["扩展情节细节并降低重复表达"],
    }
