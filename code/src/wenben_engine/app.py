"""CLI entrypoint for chapter-1 scaffold."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import asdict

from wenben_engine.core.config import Settings
from wenben_engine.core.exceptions import ConfigError
from wenben_engine.core.logging_utils import setup_logging
from wenben_engine.health.service import run_health_check

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WenBen Engine")
    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Run health check and print JSON result",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        settings = Settings.from_env()
        setup_logging(settings.log_level)
    except ConfigError as exc:
        print(f"CONFIG_ERROR: {exc}", file=sys.stderr)
        return 2

    if args.health_check:
        report = run_health_check(settings)
        print(json.dumps(asdict(report), ensure_ascii=False))
        return 0

    logger.info("Application bootstrapped. Use --health-check for chapter-1 output.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
