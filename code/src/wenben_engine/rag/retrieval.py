"""Simple retrieval utilities for chapter-7."""

from __future__ import annotations

from typing import Dict, List


def _score(query: str, text: str) -> int:
    q_terms = [t for t in query.lower().split() if t]
    return sum(1 for t in q_terms if t in text.lower())


def search_vector_context(query: str, corpus: List[Dict], top_k: int = 3) -> List[Dict]:
    ranked = []
    for item in corpus:
        text = str(item.get("text", ""))
        s = _score(query, text)
        ranked.append({"text": text, "source": item.get("source", "unknown"), "score": s})
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked[:top_k]


def fetch_recent_chapters(chapters: List[Dict], count: int = 2) -> List[Dict]:
    return list(chapters[-count:])
