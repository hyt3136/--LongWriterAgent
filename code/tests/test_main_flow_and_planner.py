import unittest

from wenben_engine.graph.main_flow import build_main_flow_nodes
from wenben_engine.graph.sequential_runner import SequentialGraphRunner
from wenben_engine.graph.state_schema import create_initial_state
from wenben_engine.graph.visualize import export_main_flow_mermaid
from wenben_engine.planner.service import normalize_request, plan_project
from wenben_engine.state.store import InMemoryStateStore


class MainFlowAndPlannerTestCase(unittest.TestCase):
    def test_normalize_and_plan(self):
        normalized = normalize_request("  写一个  修仙   小说  ")
        self.assertEqual(normalized["genre"], "xuanhuan")

        plan = plan_project(normalized)
        self.assertEqual(plan["status"], "ready")
        self.assertEqual(len(plan["tasks"]), 4)

    def test_main_flow_runner(self):
        store = InMemoryStateStore()
        run_id = "run-flow"
        state = create_initial_state("p-flow", run_id, "写一个都市小说")
        store.init_run(run_id, state)

        runner = SequentialGraphRunner(store)
        nodes = build_main_flow_nodes()
        final_state = runner.run(run_id, nodes)

        self.assertEqual(final_state["outputs"]["status"], "completed")
        self.assertEqual(final_state["control"]["last_node"], "finalize")

    def test_mermaid_export(self):
        text = export_main_flow_mermaid(["START", "normalize_request", "plan_project", "END"])
        self.assertIn("flowchart TD", text)
        self.assertIn("plan_project -. on_error .-> handle_error", text)


if __name__ == "__main__":
    unittest.main()
