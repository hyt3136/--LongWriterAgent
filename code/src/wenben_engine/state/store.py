"""In-memory versioned state store with CAS semantics."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class StateRecord:
    state: Dict[str, Any]
    version: int


class StateConflictError(RuntimeError):
    """Raised when expected state version does not match current version."""


class InMemoryStateStore:
    def __init__(self) -> None:
        self._state_by_run_id: Dict[str, Dict[str, Any]] = {}
        self._version_by_run_id: Dict[str, int] = {}
        self._events_by_run_id: Dict[str, List[Dict[str, Any]]] = {}

    def init_run(self, run_id: str, initial_state: Dict[str, Any]) -> None:
        if run_id in self._state_by_run_id:
            raise ValueError(f"run_id already exists: {run_id}")
        self._state_by_run_id[run_id] = deepcopy(initial_state)
        self._version_by_run_id[run_id] = 1
        self._events_by_run_id[run_id] = []

    def read_state(self, run_id: str) -> StateRecord:
        self._require_run(run_id)
        return StateRecord(
            state=deepcopy(self._state_by_run_id[run_id]),
            version=self._version_by_run_id[run_id],
        )

    def apply_patch(self, run_id: str, expected_version: int, patch: Dict[str, Any]) -> int:
        self._require_run(run_id)
        current_version = self._version_by_run_id[run_id]
        if expected_version != current_version:
            raise StateConflictError(
                f"version conflict: expected={expected_version}, current={current_version}"
            )

        state = self._state_by_run_id[run_id]
        for key, value in patch.items():
            state[key] = value

        new_version = current_version + 1
        self._version_by_run_id[run_id] = new_version
        if isinstance(state.get("meta"), dict):
            state["meta"]["state_version"] = new_version

        self._events_by_run_id[run_id].append(
            {
                "type": "state_patch_applied",
                "from_version": current_version,
                "to_version": new_version,
                "patch_keys": list(patch.keys()),
            }
        )
        return new_version

    def append_event(self, run_id: str, event: Dict[str, Any]) -> None:
        self._require_run(run_id)
        self._events_by_run_id[run_id].append(deepcopy(event))

    def read_events(self, run_id: str) -> List[Dict[str, Any]]:
        self._require_run(run_id)
        return deepcopy(self._events_by_run_id[run_id])

    def _require_run(self, run_id: str) -> None:
        if run_id not in self._state_by_run_id:
            raise KeyError(f"run_id not found: {run_id}")
