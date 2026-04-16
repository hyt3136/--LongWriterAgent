"""A/B result comparison helper."""

from typing import Dict


def compare_results(stable_metrics: Dict, canary_metrics: Dict) -> Dict:
    stable_success = float(stable_metrics.get("success_rate", 0.0))
    canary_success = float(canary_metrics.get("success_rate", 0.0))
    delta = canary_success - stable_success
    decision = "keep_stable"
    if delta >= 0.02:
        decision = "promote_canary"
    return {"delta_success_rate": round(delta, 4), "decision": decision}
