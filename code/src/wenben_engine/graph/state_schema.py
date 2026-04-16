"""GraphState schema for chapter-2 state/version design."""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class GraphState(TypedDict):
    meta: Dict[str, Any]
    request: Dict[str, Any]
    plan: Dict[str, Any]
    context: Dict[str, Any]
    draft: Dict[str, Any]
    quality: Dict[str, Any]
    tool_calls: List[Dict[str, Any]]
    errors: List[Dict[str, Any]]
    control: Dict[str, Any]
    outputs: Dict[str, Any]


def create_initial_state(project_id: str, run_id: str, user_request: str) -> GraphState:
    return GraphState(
        meta={
            "project_id": project_id,
            "run_id": run_id,
            "state_version": 1,
        },
        request={"raw_input": user_request},
        plan={},
        context={},
        draft={},
        quality={},
        tool_calls=[],
        errors=[],
        control={
            "sequential_mode": True,
            "stop_signal": False,
            "retry_count": 0,
        },
        outputs={},
    )
