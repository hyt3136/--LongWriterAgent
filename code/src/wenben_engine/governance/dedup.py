"""Request fingerprint deduplication."""

import hashlib
import json
from typing import Any, Dict, Set


class FingerprintDeduper:
    def __init__(self) -> None:
        self._seen: Set[str] = set()

    def _fingerprint(self, tool_name: str, args: Dict[str, Any]) -> str:
        raw = tool_name + ":" + json.dumps(args, ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def seen_before(self, tool_name: str, args: Dict[str, Any]) -> bool:
        fp = self._fingerprint(tool_name, args)
        if fp in self._seen:
            return True
        self._seen.add(fp)
        return False
