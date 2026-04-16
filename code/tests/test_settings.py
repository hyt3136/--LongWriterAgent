import os
import unittest
from unittest.mock import patch

from wenben_engine.core.config import Settings


class SettingsTestCase(unittest.TestCase):
    def test_settings_from_env_defaults(self):
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in {"APP_ENV", "APP_NAME", "APP_PORT", "LOG_LEVEL"}
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings.from_env()

        self.assertEqual(settings.app_env, "dev")
        self.assertEqual(settings.app_name, "wenben-engine")
        self.assertEqual(settings.app_port, 8080)
        self.assertEqual(settings.log_level, "INFO")

    def test_settings_from_env_custom(self):
        env = {
            "APP_ENV": "prod",
            "APP_NAME": "my-app",
            "APP_PORT": "9000",
            "LOG_LEVEL": "warning",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = Settings.from_env()

        self.assertEqual(settings.app_env, "prod")
        self.assertEqual(settings.app_name, "my-app")
        self.assertEqual(settings.app_port, 9000)
        self.assertEqual(settings.log_level, "WARNING")


if __name__ == "__main__":
    unittest.main()
