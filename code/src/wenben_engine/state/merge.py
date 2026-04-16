"""Field-level merge strategies for chapter-10."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List


def merge_append(base: List[Dict[str, Any]], incoming: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = list(deepcopy(base))
    out.extend(deepcopy(incoming))
    return out


def merge_map(base: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(deepcopy(base))
    out.update(deepcopy(incoming))
    return out


def merge_text(base: str, incoming: str, strategy: str = "candidate") -> Dict[str, Any]:
    if strategy == "candidate":
        return {"selected": base, "candidates": [base, incoming]}
    if strategy == "overwrite":
        return {"selected": incoming, "candidates": [base, incoming]}
    raise ValueError(f"unknown strategy: {strategy}")
