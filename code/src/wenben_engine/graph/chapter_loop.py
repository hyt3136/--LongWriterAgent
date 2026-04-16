"""Write-review-revise loop with early-stop for chapter generation."""

from __future__ import annotations

from typing import Dict

from wenben_engine.agents.reviewer import review_draft
from wenben_engine.agents.reviser import revise_draft
from wenben_engine.agents.writer import write_draft


def run_chapter_loop(chapter_title: str, context: Dict, max_rounds: int = 3, min_gain: float = 0.2) -> Dict:
    draft = write_draft(chapter_title, context)
    history = []
    prev_score = -1.0

    for idx in range(1, max_rounds + 1):
        review = review_draft(draft)
        history.append({"round": idx, "score": review["total_score"], "passed": review["passed"]})

        if review["passed"]:
            return {"draft": draft, "review": review, "history": history, "status": "passed"}

        gain = review["total_score"] - prev_score
        if prev_score >= 0 and gain < min_gain:
            return {"draft": draft, "review": review, "history": history, "status": "early_stop"}

        prev_score = review["total_score"]
        draft = revise_draft(draft, review, idx)

    final_review = review_draft(draft)
    history.append({"round": max_rounds + 1, "score": final_review["total_score"], "passed": final_review["passed"]})
    return {"draft": draft, "review": final_review, "history": history, "status": "max_rounds"}
