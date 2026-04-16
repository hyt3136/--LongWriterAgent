"""Chapter-level single-writer submitter."""

from __future__ import annotations

from typing import Dict

from wenben_engine.state.store import InMemoryStateStore, StateConflictError


class ChapterSubmitter:
    def __init__(self, store: InMemoryStateStore) -> None:
        self.store = store
        self._locks: Dict[str, bool] = {}

    def submit(self, run_id: str, chapter_id: str, chapter_payload: Dict) -> int:
        if self._locks.get(chapter_id):
            raise RuntimeError(f"chapter locked: {chapter_id}")

        self._locks[chapter_id] = True
        try:
            record = self.store.read_state(run_id)
            outputs = dict(record.state.get("outputs", {}))
            chapters = dict(outputs.get("chapters", {}))
            chapters[chapter_id] = chapter_payload
            outputs["chapters"] = chapters
            version = self.store.apply_patch(run_id, record.version, {"outputs": outputs})
            self.store.append_event(
                run_id,
                {"type": "chapter_submitted", "chapter_id": chapter_id, "version": version},
            )
            return version
        finally:
            self._locks[chapter_id] = False
