"""Replay tool from stored events."""

from __future__ import annotations

from typing import Dict, List


class ReplayEngine:
    def replay_node_sequence(self, events: List[Dict]) -> List[str]:
        sequence = []
        for evt in events:
            if evt.get("type") == "node_executed":
                sequence.append(str(evt.get("node_name", "")))
        return sequence
