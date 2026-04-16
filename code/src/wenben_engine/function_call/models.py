"""Function call request/response envelope models."""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class FunctionCallEnvelope:
    call_id: str
    trace_id: str
    idempotency_key: str
    tool_name: str
    arguments: Dict[str, Any]
    state_version: int


@dataclass(frozen=True)
class FunctionCallResult:
    call_id: str
    status: str
    error_code: str
    result: Dict[str, Any] = field(default_factory=dict)
