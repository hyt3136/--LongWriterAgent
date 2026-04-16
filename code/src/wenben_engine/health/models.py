"""Health check result model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthReport:
    status: str
    app_name: str
    app_env: str
    app_port: int
