import unittest
from time import time

from wenben_engine.observability.replay import ReplayEngine
from wenben_engine.observability.telemetry import TelemetryRecorder
from wenben_engine.state.merge import merge_append, merge_map, merge_text


class MergeAndObservabilityTestCase(unittest.TestCase):
    def test_merge_strategies(self):
        appended = merge_append([{"a": 1}], [{"b": 2}])
        self.assertEqual(len(appended), 2)

        merged = merge_map({"x": 1}, {"y": 2})
        self.assertEqual(merged["y"], 2)

        text = merge_text("old", "new", strategy="candidate")
        self.assertEqual(text["selected"], "old")
        self.assertEqual(len(text["candidates"]), 2)

    def test_telemetry_and_replay(self):
        recorder = TelemetryRecorder()
        recorder.record("node_a", "ok", started_at=time())
        exported = recorder.export()
        self.assertEqual(len(exported), 1)

        replay = ReplayEngine()
        seq = replay.replay_node_sequence(
            [
                {"type": "node_executed", "node_name": "normalize_request"},
                {"type": "node_executed", "node_name": "plan_project"},
            ]
        )
        self.assertEqual(seq, ["normalize_request", "plan_project"])


if __name__ == "__main__":
    unittest.main()
