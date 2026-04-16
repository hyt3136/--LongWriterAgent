"""Tool model definitions."""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class ToolResponse:
    status: str
    error_code: str
    result: Dict[str, Any] = field(default_factory=dict)


class ToolErrorCode:
    NONE = ""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    TOOL_NOT_FOUND = "TOOL_NOT_FOUND"
    EXECUTION_ERROR = "EXECUTION_ERROR"
