"""Tool registry with schema validation and structured response."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict

from wenben_engine.tools.models import ToolErrorCode, ToolResponse
from wenben_engine.tools.schema_validator import validate_args

ToolHandler = Callable[[Dict[str, Any]], Dict[str, Any]]


@dataclass(frozen=True)
class ToolSpec:
    name: str
    schema: Dict[str, Any]
    handler: ToolHandler


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self._tools[spec.name] = spec

    def invoke(self, name: str, args: Dict[str, Any]) -> ToolResponse:
        spec = self._tools.get(name)
        if spec is None:
            return ToolResponse(status="error", error_code=ToolErrorCode.TOOL_NOT_FOUND)

        err = validate_args(spec.schema, args)
        if err:
            return ToolResponse(
                status="error",
                error_code=ToolErrorCode.VALIDATION_ERROR,
                result={"message": err},
            )

        try:
            result = spec.handler(args)
            return ToolResponse(status="ok", error_code=ToolErrorCode.NONE, result=result)
        except Exception as exc:
            return ToolResponse(
                status="error",
                error_code=ToolErrorCode.EXECUTION_ERROR,
                result={"message": str(exc)},
            )
