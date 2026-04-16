"""Rollback controller."""


class RollbackManager:
    def __init__(self) -> None:
        self.current_version = "stable"

    def switch_to_canary(self) -> None:
        self.current_version = "canary"

    def rollback(self) -> None:
        self.current_version = "stable"
