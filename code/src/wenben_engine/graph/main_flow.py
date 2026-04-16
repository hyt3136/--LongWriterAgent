"""Main sequential flow nodes for chapter-3."""

from typing import Dict, List

from wenben_engine.graph.sequential_runner import GraphNode
from wenben_engine.graph.state_schema import GraphState
from wenben_engine.planner.service import normalize_request, plan_project


def node_normalize_request(state: GraphState) -> Dict:
    raw_input = str(state.get("request", {}).get("raw_input", ""))
    normalized = normalize_request(raw_input)
    return {"request": normalized}


def node_plan_project(state: GraphState) -> Dict:
    request = state.get("request", {})
    plan = plan_project(request)
    return {"plan": plan}


def node_handle_error(state: GraphState) -> Dict:
    outputs = dict(state.get("outputs", {}))
    outputs["status"] = "failed"
    control = dict(state.get("control", {}))
    control["stop_signal"] = True
    return {"outputs": outputs, "control": control}


def node_finalize(state: GraphState) -> Dict:
    outputs = dict(state.get("outputs", {}))
    outputs["status"] = "completed"
    return {"outputs": outputs}


def build_main_flow_nodes() -> List[GraphNode]:
    return [
        GraphNode(name="normalize_request", handler=node_normalize_request),
        GraphNode(name="plan_project", handler=node_plan_project),
        GraphNode(name="finalize", handler=node_finalize),
    ]
