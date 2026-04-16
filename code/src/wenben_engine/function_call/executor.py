"""Function call executor with idempotency and call log."""

from __future__ import annotations

from typing import Dict

from wenben_engine.function_call.models import FunctionCallEnvelope, FunctionCallResult
from wenben_engine.tools.models import ToolErrorCode
from wenben_engine.tools.registry import ToolRegistry


class FunctionCallExecutor:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry
        self._idempotency_results: Dict[str, FunctionCallResult] = {}
        self._logs = []

    def execute(self, envelope: FunctionCallEnvelope) -> FunctionCallResult:
        if envelope.idempotency_key in self._idempotency_results:
            cached = self._idempotency_results[envelope.idempotency_key]
            duplicate = FunctionCallResult(
                call_id=envelope.call_id,
                status="duplicate",
                error_code=cached.error_code,
                result=cached.result,
            )
            self._logs.append({"call_id": envelope.call_id, "status": "duplicate"})
            return duplicate

        tool_resp = self.registry.invoke(envelope.tool_name, envelope.arguments)
        result = FunctionCallResult(
            call_id=envelope.call_id,
            status=tool_resp.status,
            error_code=tool_resp.error_code,
            result=tool_resp.result,
        )
        self._idempotency_results[envelope.idempotency_key] = result
        self._logs.append(
            {
                "call_id": envelope.call_id,
                "trace_id": envelope.trace_id,
                "tool_name": envelope.tool_name,
                "status": result.status,
                "error_code": result.error_code,
            }
        )
        return result

    def read_logs(self):
        return list(self._logs)
