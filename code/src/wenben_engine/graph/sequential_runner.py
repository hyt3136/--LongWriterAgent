"""Sequential graph runner for single-model environments.

Design rule: execute exactly one node at a time, in deterministic order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List

from wenben_engine.state.store import InMemoryStateStore

NodeFn = Callable[[Dict[str, Any]], Dict[str, Any]]


@dataclass(frozen=True)
class GraphNode:
    name: str
    handler: NodeFn


class SequentialGraphRunner:
    def __init__(self, store: InMemoryStateStore) -> None:
        self.store = store

    def run(self, run_id: str, nodes: List[GraphNode]) -> Dict[str, Any]:
        for node in nodes:
            record = self.store.read_state(run_id)
            current_state = record.state

            patch = node.handler(current_state)
            if not isinstance(patch, dict):
                raise TypeError(f"node {node.name} must return dict patch")

            patch = dict(patch)
            node_control = patch.get("control", {})
            if node_control is None:
                node_control = {}
            if not isinstance(node_control, dict):
                raise TypeError(f"node {node.name} returned invalid control patch")

            control = dict(current_state.get("control", {}))
            control.update(node_control)
            control["last_node"] = node.name
            patch["control"] = control

            self.store.apply_patch(run_id, record.version, patch)
            self.store.append_event(
                run_id,
                {
                    "type": "node_executed",
                    "node_name": node.name,
                },
            )

            new_state = self.store.read_state(run_id).state
            if new_state.get("control", {}).get("stop_signal"):
                break

        return self.store.read_state(run_id).state
