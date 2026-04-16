"""Release router for stable/canary traffic split."""

import hashlib


class ReleaseRouter:
    def __init__(self, canary_percent: int = 10) -> None:
        if canary_percent < 0 or canary_percent > 100:
            raise ValueError("canary_percent must be in [0, 100]")
        self.canary_percent = canary_percent

    def route(self, key: str) -> str:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        bucket = int(digest[:8], 16) % 100
        return "canary" if bucket < self.canary_percent else "stable"
