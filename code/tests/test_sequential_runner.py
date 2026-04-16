import unittest

from wenben_engine.graph.sequential_runner import GraphNode, SequentialGraphRunner
from wenben_engine.graph.state_schema import create_initial_state
from wenben_engine.state.store import InMemoryStateStore


class SequentialRunnerTestCase(unittest.TestCase):
    def test_run_nodes_in_order(self):
        store = InMemoryStateStore()
        run_id = "run-seq"
        store.init_run(run_id, create_initial_state("p3", run_id, "idea"))

        def node_plan(state):
            return {"plan": {"done": True}}

        def node_stop(state):
            control = dict(state.get("control", {}))
            control["stop_signal"] = True
            return {"control": control}

        def node_should_not_run(state):
            return {"outputs": {"bad": True}}

        runner = SequentialGraphRunner(store)
        runner.run(
            run_id,
            [
                GraphNode(name="plan", handler=node_plan),
                GraphNode(name="stop", handler=node_stop),
                GraphNode(name="should_not_run", handler=node_should_not_run),
            ],
        )

        state = store.read_state(run_id).state
        self.assertTrue(state["plan"]["done"])
        self.assertNotIn("bad", state["outputs"])
        self.assertEqual(state["control"]["last_node"], "stop")


if __name__ == "__main__":
    unittest.main()
