"""Environment-backed application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass

from wenben_engine.core.exceptions import ConfigError

_ALLOWED_ENV = {"dev", "test", "prod"}
_ALLOWED_LOG_LEVEL = {"DEBUG", "INFO", "WARNING", "ERROR"}


@dataclass(frozen=True)
class Settings:
    app_env: str
    app_name: str
    app_port: int
    log_level: str


    @staticmethod
    def from_env() -> "Settings":
        app_env = os.getenv("APP_ENV", "dev").strip().lower()
        app_name = os.getenv("APP_NAME", "wenben-engine").strip()
        app_port_raw = os.getenv("APP_PORT", "8080").strip()
        log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()

        if app_env not in _ALLOWED_ENV:
            raise ConfigError(f"APP_ENV must be one of {_ALLOWED_ENV}, got: {app_env}")

        if not app_name:
            raise ConfigError("APP_NAME must not be empty")

        if not app_port_raw.isdigit():
            raise ConfigError(f"APP_PORT must be a number, got: {app_port_raw}")

        app_port = int(app_port_raw)
        if app_port < 1 or app_port > 65535:
            raise ConfigError(f"APP_PORT must be in [1, 65535], got: {app_port}")

        if log_level not in _ALLOWED_LOG_LEVEL:
            raise ConfigError(
                f"LOG_LEVEL must be one of {_ALLOWED_LOG_LEVEL}, got: {log_level}"
            )

        return Settings(
            app_env=app_env,
            app_name=app_name,
            app_port=app_port,
            log_level=log_level,
        )
