"""Node-level telemetry recording."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from time import time
from typing import Dict, List


@dataclass
class TelemetryEvent:
    node_name: str
    status: str
    started_at: float
    ended_at: float
    error_code: str = ""


class TelemetryRecorder:
    def __init__(self) -> None:
        self._events: List[TelemetryEvent] = []

    def record(self, node_name: str, status: str, started_at: float, error_code: str = "") -> None:
        self._events.append(
            TelemetryEvent(
                node_name=node_name,
                status=status,
                started_at=started_at,
                ended_at=time(),
                error_code=error_code,
            )
        )

    def export(self) -> List[Dict]:
        return [asdict(evt) for evt in self._events]
