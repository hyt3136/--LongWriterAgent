"""Invalid call guard with fuse threshold."""


class InvalidCallGuard:
    def __init__(self, threshold: int = 3) -> None:
        self.threshold = threshold
        self.count = 0

    def record_invalid(self) -> None:
        self.count += 1

    def reset(self) -> None:
        self.count = 0

    def should_halt(self) -> bool:
        return self.count >= self.threshold
