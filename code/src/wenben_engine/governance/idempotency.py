"""Idempotency key manager."""

from typing import Dict


class IdempotencyStore:
    def __init__(self) -> None:
        self._keys: Dict[str, str] = {}

    def claim(self, key: str, value: str) -> bool:
        if key in self._keys:
            return False
        self._keys[key] = value
        return True

    def get(self, key: str) -> str:
        return self._keys.get(key, "")
