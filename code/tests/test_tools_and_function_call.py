import unittest

from wenben_engine.function_call.executor import FunctionCallExecutor
from wenben_engine.function_call.models import FunctionCallEnvelope
from wenben_engine.tools.registry import ToolRegistry, ToolSpec


class ToolsAndFunctionCallTestCase(unittest.TestCase):
    def test_tool_validation(self):
        registry = ToolRegistry()
        registry.register(
            ToolSpec(
                name="sum_tool",
                schema={
                    "required": ["a", "b"],
                    "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
                },
                handler=lambda x: {"sum": x["a"] + x["b"]},
            )
        )

        bad = registry.invoke("sum_tool", {"a": 1})
        self.assertEqual(bad.status, "error")

        ok = registry.invoke("sum_tool", {"a": 1, "b": 2})
        self.assertEqual(ok.status, "ok")
        self.assertEqual(ok.result["sum"], 3)

    def test_function_call_duplicate(self):
        registry = ToolRegistry()
        registry.register(
            ToolSpec(
                name="echo_tool",
                schema={"required": ["text"], "properties": {"text": {"type": "string"}}},
                handler=lambda x: {"text": x["text"]},
            )
        )

        executor = FunctionCallExecutor(registry)
        first = executor.execute(
            FunctionCallEnvelope(
                call_id="c1",
                trace_id="t1",
                idempotency_key="k1",
                tool_name="echo_tool",
                arguments={"text": "hello"},
                state_version=1,
            )
        )
        second = executor.execute(
            FunctionCallEnvelope(
                call_id="c2",
                trace_id="t1",
                idempotency_key="k1",
                tool_name="echo_tool",
                arguments={"text": "hello"},
                state_version=1,
            )
        )

        self.assertEqual(first.status, "ok")
        self.assertEqual(second.status, "duplicate")


if __name__ == "__main__":
    unittest.main()
