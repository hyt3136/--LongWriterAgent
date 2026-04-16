"""Domain-safe exceptions for predictable error handling."""


class ConfigError(ValueError):
    """Raised when environment configuration is invalid."""
