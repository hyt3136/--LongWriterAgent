"""Graph visualization helpers."""

from typing import List


def export_main_flow_mermaid(nodes: List[str]) -> str:
    lines = ["flowchart TD"]
    for i in range(len(nodes) - 1):
        lines.append(f"  {nodes[i]} --> {nodes[i + 1]}")
    lines.append("  plan_project -. on_error .-> handle_error")
    lines.append("  chapter_loop -. on_error .-> handle_error")
    return "\n".join(lines)
