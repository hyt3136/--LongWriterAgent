"""Minimal JSON-like schema validator without third-party dependencies."""

from typing import Any, Dict


_TYPE_MAP = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "object": dict,
    "array": list,
}


def validate_args(schema: Dict[str, Any], args: Dict[str, Any]) -> str:
    required = schema.get("required", [])
    properties = schema.get("properties", {})

    for key in required:
        if key not in args:
            return f"missing required field: {key}"

    for key, spec in properties.items():
        if key not in args:
            continue
        expected_type = spec.get("type")
        if expected_type in _TYPE_MAP and not isinstance(args[key], _TYPE_MAP[expected_type]):
            return f"field {key} expected {expected_type}"

        if "enum" in spec and args[key] not in spec["enum"]:
            return f"field {key} not in enum"

    return ""
