import unittest

from wenben_engine.governance.dedup import FingerprintDeduper
from wenben_engine.governance.idempotency import IdempotencyStore
from wenben_engine.governance.invalid_guard import InvalidCallGuard
from wenben_engine.release.ab_compare import compare_results
from wenben_engine.release.rollback import RollbackManager
from wenben_engine.release.router import ReleaseRouter


class GovernanceAndReleaseTestCase(unittest.TestCase):
    def test_idempotency_and_dedup(self):
        store = IdempotencyStore()
        self.assertTrue(store.claim("k1", "v1"))
        self.assertFalse(store.claim("k1", "v2"))

        deduper = FingerprintDeduper()
        self.assertFalse(deduper.seen_before("tool", {"a": 1}))
        self.assertTrue(deduper.seen_before("tool", {"a": 1}))

    def test_invalid_guard(self):
        guard = InvalidCallGuard(threshold=2)
        guard.record_invalid()
        self.assertFalse(guard.should_halt())
        guard.record_invalid()
        self.assertTrue(guard.should_halt())

    def test_release_components(self):
        router = ReleaseRouter(canary_percent=100)
        self.assertEqual(router.route("user-1"), "canary")

        compare = compare_results({"success_rate": 0.9}, {"success_rate": 0.93})
        self.assertEqual(compare["decision"], "promote_canary")

        rollback = RollbackManager()
        rollback.switch_to_canary()
        self.assertEqual(rollback.current_version, "canary")
        rollback.rollback()
        self.assertEqual(rollback.current_version, "stable")


if __name__ == "__main__":
    unittest.main()
