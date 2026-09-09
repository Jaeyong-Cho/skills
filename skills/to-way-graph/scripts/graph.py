#!/usr/bin/env python3
"""Validation and Markdown rendering helpers for to-way-graph."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

TASK_KINDS = {"EXPLORE", "EXPERIMENT", "IMPL", "CHECKOUT"}
STATUSES = {"ready", "in-progress", "waiting", "blocked", "done"}
REQUIRED_NODE_FIELDS = (
    "title",
    "description",
    "parent",
    "children",
    "purpose",
    "current_state",
    "expected_result_state",
    "hypothesis",
    "assumptions",
)
REQUIRED_WAY_FIELDS = ("success",)
REQUIRED_TASK_FIELDS = (
    "task_kind",
    "why",
    "what",
    "expected_result_state",
    "how",
    "status",
    "workdir",
    "done_when",
)


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, indent=2)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _has_state_example(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    fence = None
    content = []
    for line in value.splitlines():
        if fence is None:
            opening = re.fullmatch(r" {0,3}(`{3,}|~{3,})(.*)", line)
            if opening and not (opening[1][0] == "`" and "`" in opening[2]):
                fence = opening[1]
                content = []
        elif re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}[ \t]*", line):
            if "\n".join(content).strip():
                return True
            fence = None
        else:
            content.append(line)
    return False


def _safe_relative(value: Any) -> bool:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        return False
    path = Path(value)
    return ".." not in path.parts


def validate(document: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["document must be an object"]
    if document.get("version") != 1:
        errors.append("version must be 1")
    goals = document.get("goals")
    nodes = document.get("nodes")
    edges = document.get("edges")
    if not isinstance(goals, list) or not goals:
        errors.append("goals must be a non-empty list")
    if not isinstance(nodes, dict) or not nodes:
        errors.append("nodes must be a non-empty object")
    if not isinstance(edges, dict):
        errors.append("edges must be an object")
    if errors:
        return errors

    node_ids = set(nodes)
    for node_id, node in nodes.items():
        prefix = f"nodes.{node_id}"
        if not isinstance(node, dict):
            errors.append(f"{prefix} must be an object")
            continue
        node_type = node.get("type")
        if node_type not in {"way", "task"}:
            errors.append(f"{prefix}.type must be way or task")
        for field in REQUIRED_NODE_FIELDS:
            if field not in node:
                errors.append(f"{prefix}.{field} is required")
        for field in ("current_state", "expected_result_state"):
            if field in node and not _has_state_example(node[field]):
                errors.append(f"{prefix}.{field} must be a Markdown string with a non-empty, closed fenced code block showing a concrete state example")
        if not _nonempty(node.get("title")):
            errors.append(f"{prefix}.title must be a non-empty string")
        if not isinstance(node.get("children"), list):
            errors.append(f"{prefix}.children must be a list")
        else:
            if len(node["children"]) != len(set(node["children"])):
                errors.append(f"{prefix}.children contains duplicates")
            for child in node["children"]:
                if child not in node_ids:
                    errors.append(f"{prefix}.children references unknown node {child}")
        parent = node.get("parent")
        if parent is not None and parent not in node_ids:
            errors.append(f"{prefix}.parent references unknown node {parent}")
        elif parent is not None and isinstance(nodes.get(parent), dict) and nodes[parent].get("type") != "way":
            errors.append(f"{prefix}.parent must be a way")
        if node_type == "way":
            for field in REQUIRED_WAY_FIELDS:
                if field not in node:
                    errors.append(f"{prefix}.{field} is required")
            if not _safe_relative(node.get("file")) or not str(node["file"]).endswith(".md"):
                errors.append(f"{prefix}.file must be a relative Markdown path")
            if not isinstance(node.get("position"), int) or node["position"] < 0:
                errors.append(f"{prefix}.position must be a non-negative integer")
        elif node_type == "task":
            if node.get("children"):
                errors.append(f"{prefix}.task nodes cannot have children")
            for field in REQUIRED_TASK_FIELDS:
                if field not in node:
                    errors.append(f"{prefix}.{field} is required")
            if node.get("task_kind") not in TASK_KINDS:
                errors.append(f"{prefix}.task_kind must be one of {sorted(TASK_KINDS)}")
            if node.get("status") not in STATUSES:
                errors.append(f"{prefix}.status must be one of {sorted(STATUSES)}")
            workdir = node.get("workdir")
            if not isinstance(workdir, str) or not Path(workdir).is_absolute() or Path(workdir).name != node_id:
                errors.append(f"{prefix}.workdir must be an absolute directory ending in {node_id}")
            target = node.get("target_repo")
            if node.get("task_kind") == "IMPL":
                if not isinstance(target, str) or not Path(target).is_absolute():
                    errors.append(f"{prefix}.target_repo must be absolute for IMPL tasks")
            elif target is not None:
                errors.append(f"{prefix}.target_repo is only allowed for IMPL tasks")

    root_ids = document.get("root_ids")
    if not isinstance(root_ids, list) or not root_ids:
        errors.append("root_ids must be a non-empty list")
        root_ids = []
    if len(root_ids) != len(set(root_ids)):
        errors.append("root_ids contains duplicates")
    for root in root_ids:
        if root not in node_ids:
            errors.append(f"root_ids references unknown node {root}")
        elif nodes[root].get("parent") is not None:
            errors.append(f"root node {root} must have parent null")
        elif nodes[root].get("type") != "way":
            errors.append(f"root node {root} must be a way")
    actual_roots = {node_id for node_id, node in nodes.items() if node.get("parent") is None}
    if set(root_ids) != actual_roots:
        errors.append("root_ids must exactly match nodes with parent null")

    contains = edges.get("contains")
    depends = edges.get("depends_on")
    if not isinstance(contains, list):
        errors.append("edges.contains must be a list")
        contains = []
    if not isinstance(depends, list):
        errors.append("edges.depends_on must be a list")
        depends = []

    contained_pairs: set[tuple[str, str]] = set()
    for edge in contains:
        if not isinstance(edge, dict) or set(edge) != {"from", "to"}:
            errors.append("each containment edge must have from and to")
            continue
        source, target = edge["from"], edge["to"]
        pair = (source, target)
        if source not in node_ids or target not in node_ids:
            errors.append(f"containment edge references unknown node: {source} -> {target}")
        if pair in contained_pairs:
            errors.append(f"duplicate containment edge: {source} -> {target}")
        contained_pairs.add(pair)
    expected_pairs = {
        (node_id, child)
        for node_id, node in nodes.items()
        for child in node.get("children", [])
    }
    if contained_pairs != expected_pairs:
        errors.append("edges.contains must exactly match every node's children list")
    for node_id, node in nodes.items():
        for child in node.get("children", []):
            if nodes.get(child, {}).get("parent") != node_id:
                errors.append(f"{node_id} child {child} has a mismatched parent")

    dependency_pairs: set[tuple[str, str]] = set()
    graph: dict[str, set[str]] = {node_id: set() for node_id in node_ids}
    for edge in depends:
        if not isinstance(edge, dict) or set(edge) != {"from", "to"}:
            errors.append("each dependency edge must have from and to")
            continue
        source, target = edge["from"], edge["to"]
        pair = (source, target)
        if source not in node_ids or target not in node_ids:
            errors.append(f"dependency edge references unknown node: {source} -> {target}")
        if source == target:
            errors.append(f"dependency edge cannot self-reference: {source}")
        if pair in dependency_pairs:
            errors.append(f"duplicate dependency edge: {source} -> {target}")
        dependency_pairs.add(pair)
        if source in graph and target in graph:
            graph[source].add(target)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visiting:
            errors.append(f"dependency cycle includes {node_id}")
            return
        if node_id in visited:
            return
        visiting.add(node_id)
        for prerequisite in graph[node_id]:
            visit(prerequisite)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in node_ids:
        visit(node_id)

    directories: set[str] = set()
    if len(goals) != len(set(goals)):
        errors.append("goals contains duplicates")
    for goal in goals:
        if not isinstance(goal, str) or goal not in node_ids:
            errors.append(f"goals references unknown node {goal}")
            continue
        if nodes[goal].get("type") != "way" or nodes[goal].get("parent") is not None:
            errors.append(f"goal {goal} must be a root way")
        directory = nodes[goal].get("directory")
        if not _safe_relative(directory):
            errors.append(f"root way {goal}.directory must be a relative path")
        elif directory in directories:
            errors.append(f"duplicate goal directory: {directory}")
        else:
            directories.add(directory)

    for node_id, node in nodes.items():
        if node.get("type") == "way" and node.get("file") == "0-goal.md" and node_id not in root_ids:
            errors.append(f"only root ways may use 0-goal.md: {node_id}")

    for root in root_ids:
        files: set[str] = set()
        stack = [root]
        while stack:
            node_id = stack.pop()
            node = nodes[node_id]
            if node.get("type") == "way":
                file = node.get("file")
                if file in files:
                    errors.append(f"duplicate Markdown file within goal {root}: {file}")
                files.add(file)
            stack.extend(node.get("children", []))

    reachable: set[str] = set()
    stack = list(root_ids)
    while stack:
        node_id = stack.pop()
        if node_id in reachable:
            continue
        reachable.add(node_id)
        stack.extend(nodes[node_id].get("children", []))
    if reachable != node_ids:
        errors.append("every node must be reachable from root_ids through containment")

    return errors


def _yaml(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def _lines(value: Any, indent: int = 0) -> list[str]:
    prefix = " " * indent
    if isinstance(value, list):
        return [f"{prefix}- {_text(item)}" for item in value]
    if isinstance(value, dict):
        return [f"{prefix}{key}: {_text(item)}" for key, item in value.items()]
    return [prefix + _text(value)]


def _state_field(label: str, value: str) -> str:
    return f"- {label}:\n\n" + "\n".join("  " + line if line else "" for line in value.splitlines())


def _slug_title(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip()


def render(document: dict[str, Any], goal_id: str) -> dict[str, str]:
    nodes = document["nodes"]
    dependencies: dict[str, list[str]] = {node_id: [] for node_id in nodes}
    for edge in document["edges"]["depends_on"]:
        dependencies[edge["from"]].append(edge["to"])

    def file_for(node_id: str) -> str:
        node = nodes[node_id]
        if node["type"] == "way":
            return node["file"]
        return file_for(node["parent"])

    def link(from_file: str, node_id: str) -> str:
        target_file = file_for(node_id)
        relative = Path(target_file)
        if from_file != target_file:
            relative = Path(__import__("os").path.relpath(target_file, Path(from_file).parent or "."))
        suffix = f"#{node_id}" if nodes[node_id]["type"] == "task" else ""
        return f"[{node_id}]({relative.as_posix()}{suffix})"

    def frontmatter(node: dict[str, Any]) -> list[str]:
        data = node.get("frontmatter", {})
        data = {
            "type": "Way Group",
            "title": node["title"],
            "description": node["description"],
            "tags": ["wayfinder", "task-plan"],
            **data,
        }
        return ["---"] + [f"{key}: {_yaml(value)}" for key, value in data.items()] + ["---", ""]

    def outcome(node_id: str, node: dict[str, Any]) -> list[str]:
        lines = ["## Outcome", f"- ID: {node_id}", f"- Position: {node['position']}"]
        if node.get("parent") is not None:
            lines.append(f"- Parent: {link(node['file'], node['parent'])}")
        lines += [
            f"- Purpose: {_text(node['purpose'])}",
            _state_field("Current state", node["current_state"]),
            _state_field("Expected result state", node["expected_result_state"]),
            f"- Hypothesis: {_text(node['hypothesis'])}",
            f"- Assumptions: {_text(node['assumptions'])}",
        ]
        if "success" in node:
            lines.append(f"- Success: {_text(node['success'])}")
        if "scope_status" in node:
            lines.append(f"- Scope/status: {_text(node['scope_status'])}")
        if dependencies[node_id]:
            lines.append(f"- Needs: {', '.join(link(node['file'], item) for item in dependencies[node_id])}")
        return lines + [""]

    def task_section(task_id: str, task: dict[str, Any], owner_file: str) -> list[str]:
        lines = [f'<a id="{task_id}"></a>', f"### {task_id} — {_slug_title(task['title'])}"]
        fields = [
            ("Kind", task["task_kind"]),
            ("Current state", task["current_state"]),
            ("Why", task["why"]),
            ("What", task["what"]),
            ("Expected result state", task["expected_result_state"]),
            ("How", task["how"]),
        ]
        prerequisite_ids = dependencies[task_id]
        needs = " — " if not prerequisite_ids else ", ".join(link(owner_file, item) for item in prerequisite_ids)
        fields += [("Needs", needs), ("Status", task["status"]), ("Workdir", task["workdir"])]
        if task["task_kind"] == "IMPL":
            fields.append(("Target repo", task["target_repo"]))
        if "evidence" in task:
            fields.append(("Evidence", task["evidence"]))
        fields.append(("Done when", task["done_when"]))
        if "conditions_conflicts" in task:
            fields.append(("Conditions/conflicts", task["conditions_conflicts"]))
        for label, value in fields:
            if label in ("Current state", "Expected result state"):
                lines.append(_state_field(label, value))
            elif label == "How" and isinstance(value, list):
                lines.append("- How:")
                lines.extend(f"  {index}. {_text(item)}" for index, item in enumerate(value, 1))
            else:
                lines.append(f"- {label}: {_text(value)}")
        uncertainty = task.get("uncertainty")
        if uncertainty:
            lines.append("")
            for key, value in uncertainty.items():
                lines.append(f"- {key.replace('_', ' ').title()}: {_text(value)}")
        return lines + [""]

    def tree_line(node_id: str, owner_file: str, depth: int = 0) -> list[str]:
        node = nodes[node_id]
        marker = "  " * depth + "- "
        lines = [marker + (link(owner_file, node_id) if node["type"] == "task" else f"[{node_id} — {node['title']}]({node['file']})")]
        for child in node["children"]:
            lines.extend(tree_line(child, owner_file, depth + 1))
        return lines

    output: dict[str, str] = {}
    for node_id, node in nodes.items():
        if node["type"] != "way" or not (node_id == goal_id or _is_descendant(node_id, goal_id, nodes)):
            continue
        lines = frontmatter(node) + [f"# {node['title']}", ""] + outcome(node_id, node) + ["## Work", ""]
        for child in node["children"]:
            child_node = nodes[child]
            if child_node["type"] == "way":
                lines.append(f"- {link(node['file'], child)}")
            else:
                lines.extend(task_section(child, child_node, node["file"]))
        if node_id == goal_id:
            lines += ["## Grounding", ""] + _lines(node.get("grounding", "—")) + ["", "## Way tree", ""]
            lines += tree_line(goal_id, node["file"])[1:] + ["", "## Execution", ""]
            lines += _lines(node.get("execution", "—"))
        if node.get("context_and_uncertainties"):
            lines += ["", "## Context and uncertainties", ""] + _lines(node["context_and_uncertainties"])
        output[node["file"]] = "\n".join(lines).rstrip() + "\n"
    return output


def _is_descendant(node_id: str, root_id: str, nodes: dict[str, Any]) -> bool:
    current = nodes[node_id].get("parent")
    while current is not None:
        if current == root_id:
            return True
        current = nodes[current].get("parent")
    return False
