#!/usr/bin/env python3
# ---
# type: Python Script
# title: Lint Way Graph JSON
# description: Validate the JSON graph emitted by the to-way skill.
# tags: [wayfinder, validation, json]
# timestamp: 2026-09-07T21:52:08+09:00
# ---
"""Lint a to-way route graph JSON file.

Usage:
  python3 lint_graph.py <graph.json>
  python3 lint_graph.py --test

Exit code 0 means the graph is valid; exit code 1 reports violations.
"""

import json
import sys
from pathlib import Path

KINDS = {"goal", "checkpoint", "task", "experiment", "exploration"}
EDGE_TYPES = {"decomposes", "depends_on"}


def text(value):
    return isinstance(value, str) and bool(value.strip())


def lint(graph):
    errors = []
    if not isinstance(graph, dict):
        return ["root must be an object"]

    if not text(graph.get("intent")):
        errors.append("intent must be a non-empty string")
    goal_id = graph.get("goalId")
    if not text(goal_id):
        errors.append("goalId must be a non-empty string")

    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or not nodes:
        errors.append("nodes must be a non-empty array")
        nodes = []
    if not isinstance(edges, list):
        errors.append("edges must be an array")
        edges = []
    if not isinstance(graph.get("deferred"), list):
        errors.append("deferred must be an array")

    node_ids = set()
    node_by_id = {}
    goals = []
    for index, node in enumerate(nodes, start=1):
        label = f"nodes[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in ("id", "kind", "title", "description"):
            if not text(node.get(field)):
                errors.append(f"{label}.{field} must be a non-empty string")
        node_id = node.get("id")
        if text(node_id):
            if node_id in node_ids:
                errors.append(f"duplicate node id: {node_id}")
            node_ids.add(node_id)
            node_by_id[node_id] = node
        if node.get("kind") not in KINDS:
            errors.append(f"{label}.kind must be one of: {', '.join(sorted(KINDS))}")
        if node.get("kind") == "goal":
            goals.append(node_id)

    if len(goals) != 1:
        errors.append(f"graph must contain exactly one goal node, found {len(goals)}")
    elif goal_id != goals[0]:
        errors.append("goalId must reference the goal node")

    edge_ids = set()
    all_ids = set(node_ids)
    decomposes_in = {node_id: 0 for node_id in node_ids}
    adjacency = {node_id: [] for node_id in node_ids}
    for index, edge in enumerate(edges, start=1):
        label = f"edges[{index}]"
        if not isinstance(edge, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in ("id", "from", "to", "type", "description"):
            if not text(edge.get(field)):
                errors.append(f"{label}.{field} must be a non-empty string")
        edge_id = edge.get("id")
        if text(edge_id):
            if edge_id in edge_ids:
                errors.append(f"duplicate edge id: {edge_id}")
            if edge_id in all_ids:
                errors.append(f"node and edge IDs must be globally unique: {edge_id}")
            edge_ids.add(edge_id)
            all_ids.add(edge_id)
        edge_type = edge.get("type")
        if edge_type not in EDGE_TYPES:
            errors.append(f"{label}.type must be one of: {', '.join(sorted(EDGE_TYPES))}")
        source = edge.get("from")
        target = edge.get("to")
        if source not in node_ids or target not in node_ids:
            errors.append(f"{label} must reference existing node IDs")
        elif source == target:
            errors.append(f"{label} cannot connect a node to itself")
        else:
            adjacency[source].append(target)
            if edge_type == "decomposes":
                decomposes_in[target] += 1
        if "condition" in edge and edge["condition"] is not None and not text(edge["condition"]):
            errors.append(f"{label}.condition must be a non-empty string when present")

    if goals and goals[0] in node_ids:
        root = goals[0]
        if decomposes_in[root] != 0:
            errors.append("goal node must not have a decomposes parent")
        for node_id in node_ids - {root}:
            if decomposes_in[node_id] != 1:
                errors.append(f"node {node_id} must have exactly one decomposes parent")

        reachable = set()
        stack = [root]
        while stack:
            current = stack.pop()
            if current in reachable:
                continue
            reachable.add(current)
            stack.extend(
                edge.get("to")
                for edge in edges
                if isinstance(edge, dict)
                and edge.get("type") == "decomposes"
                and edge.get("from") == current
            )
        missing = node_ids - reachable
        if missing:
            errors.append(f"nodes not reachable from goal by decomposes edges: {', '.join(sorted(missing))}")

    visiting = set()
    visited = set()

    def visit(node_id):
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        if any(visit(child) for child in adjacency.get(node_id, [])):
            return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    if any(visit(node_id) for node_id in node_ids):
        errors.append("graph edges must not contain a cycle")
    return errors


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8")), []
    except json.JSONDecodeError as exc:
        return None, [f"invalid JSON: line {exc.lineno}, column {exc.colno}: {exc.msg}"]
    except OSError as exc:
        return None, [str(exc)]


def self_test():
    valid = {
        "intent": "Reach the goal safely",
        "goalId": "goal-1",
        "nodes": [
            {"id": "goal-1", "kind": "goal", "title": "Goal", "description": "The desired result."},
            {"id": "way-1", "kind": "checkpoint", "title": "Way", "description": "A high-level route."},
            {"id": "task-1", "kind": "task", "title": "Task", "description": "An actionable leaf."},
        ],
        "edges": [
            {"id": "edge-1", "from": "goal-1", "to": "way-1", "type": "decomposes", "description": "The goal has this route."},
            {"id": "edge-2", "from": "way-1", "to": "task-1", "type": "decomposes", "description": "The route requires this task."},
        ],
        "deferred": [],
    }
    assert not lint(valid)

    invalid = dict(valid)
    invalid["edges"] = [dict(valid["edges"][0], to="missing")]
    assert lint(invalid)
    print("self-test passed")


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--test":
        self_test()
        return 0
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    graph, errors = load(sys.argv[1])
    if errors:
        for error in errors:
            print(error)
        print(f"FAIL — {len(errors)} violation(s)")
        return 1
    errors = lint(graph)
    if errors:
        for error in errors:
            print(error)
        print(f"FAIL — {len(errors)} violation(s)")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
