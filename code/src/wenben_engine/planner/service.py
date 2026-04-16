"""Planner service: normalize request and build executable project plan."""

from __future__ import annotations

from typing import Dict, List


def normalize_request(user_input: str) -> Dict:
    text = " ".join(user_input.strip().split())
    genre = "unknown"
    if "科幻" in text:
        genre = "sci_fi"
    elif "玄幻" in text or "修仙" in text:
        genre = "xuanhuan"
    elif "都市" in text:
        genre = "urban"

    return {
        "raw_input": user_input,
        "normalized_input": text,
        "genre": genre,
        "target_chapters": 3,
    }


def _task(task_id: str, name: str, depends_on: List[str]) -> Dict:
    return {
        "task_id": task_id,
        "name": name,
        "depends_on": depends_on,
        "priority": "normal",
    }


def plan_project(request: Dict) -> Dict:
    normalized = str(request.get("normalized_input", "")).strip()
    if not normalized:
        return {
            "status": "invalid",
            "tasks": [],
            "reason": "empty_request",
        }

    tasks = [
        _task("t1", "outline", []),
        _task("t2", "characters", ["t1"]),
        _task("t3", "world", ["t1"]),
        _task("t4", "chapter_plan", ["t1", "t2", "t3"]),
    ]

    return {
        "status": "ready",
        "genre": request.get("genre", "unknown"),
        "target_chapters": int(request.get("target_chapters", 3)),
        "tasks": tasks,
    }
