import unittest

from wenben_engine.graph.state_schema import create_initial_state
from wenben_engine.state.store import InMemoryStateStore, StateConflictError


class StateStoreTestCase(unittest.TestCase):
    def test_apply_patch_success(self):
        store = InMemoryStateStore()
        run_id = "run-1"
        store.init_run(run_id, create_initial_state("p1", run_id, "hello"))

        record = store.read_state(run_id)
        new_version = store.apply_patch(
            run_id,
            expected_version=record.version,
            patch={"plan": {"stage": "planned"}},
        )

        self.assertEqual(new_version, 2)
        final_state = store.read_state(run_id).state
        self.assertEqual(final_state["plan"]["stage"], "planned")
        self.assertEqual(final_state["meta"]["state_version"], 2)

    def test_apply_patch_conflict(self):
        store = InMemoryStateStore()
        run_id = "run-2"
        store.init_run(run_id, create_initial_state("p2", run_id, "hello"))

        with self.assertRaises(StateConflictError):
            store.apply_patch(
                run_id,
                expected_version=99,
                patch={"plan": {"stage": "planned"}},
            )


if __name__ == "__main__":
    unittest.main()
