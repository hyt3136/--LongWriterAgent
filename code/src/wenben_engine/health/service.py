"""Health service for chapter-1 baseline observability."""

from wenben_engine.core.config import Settings
from wenben_engine.health.models import HealthReport


def run_health_check(settings: Settings) -> HealthReport:
    # In chapter 1, health only verifies configuration bootstraps correctly.
    return HealthReport(
        status="ok",
        app_name=settings.app_name,
        app_env=settings.app_env,
        app_port=settings.app_port,
    )
