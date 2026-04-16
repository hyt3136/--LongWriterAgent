"""Deterministic routes for sequential graph execution."""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class RouteDecision:
    next_node: str
    reason: str


def route_after_plan(state: Dict) -> RouteDecision:
    if state.get("errors"):
        return RouteDecision(next_node="handle_error", reason="errors_present")
    return RouteDecision(next_node="chapter_loop", reason="plan_ready")


def route_after_chapter_loop(state: Dict) -> RouteDecision:
    if state.get("errors"):
        return RouteDecision(next_node="handle_error", reason="chapter_loop_failed")
    return RouteDecision(next_node="finalize", reason="chapter_loop_passed")
