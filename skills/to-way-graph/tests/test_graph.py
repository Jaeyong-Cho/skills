import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from graph import render, validate  # noqa: E402


class GraphTests(unittest.TestCase):
    def document(self):
        way = lambda title, parent, position, file, children: {
            "type": "way", "title": title, "description": title,
            "parent": parent, "children": children, "purpose": "p",
            "current_state": "Known baseline.\n\n```text\nGraph -> raw JSON\n```",
            "expected_result_state": "Expected target.\n\n```text\nGraph -> map + details\n```",
            "hypothesis": "h", "assumptions": "—", "success": "done", "position": position,
            "file": file,
        }
        return {
            "version": 1,
            "goals": ["G"],
            "root_ids": ["G"],
            "nodes": {
                "G": {**way("Goal", None, 0, "0-goal.md", ["A", "B"]), "directory": "01-goal"},
                "A": way("A", "G", 1, "0-goal/1-1-a.md", ["A1"]),
                "A1": {
                    "type": "task", "title": "Task A1", "description": "task",
                    "parent": "A", "children": [], "purpose": "p",
                    "current_state": "Known baseline.\n\n```javascript\nreturn input;\n```",
                    "expected_result_state": "Expected target.\n\n```javascript\nvalidate(input);\nreturn input;\n```",
                    "hypothesis": "h", "assumptions": "—", "task_kind": "EXPLORE",
                    "why": "w", "what": "what", "how": ["inspect"],
                    "status": "ready", "workdir": "/tmp/A1", "done_when": "done",
                },
                "B": way("B", "G", 2, "0-goal/2-2-b.md", []),
            },
            "edges": {
                "contains": [
                    {"from": "G", "to": "A"}, {"from": "G", "to": "B"},
                    {"from": "A", "to": "A1"},
                ],
                "depends_on": [{"from": "B", "to": "A1"}],
            },
        }

    def test_valid_graph_renders_nested_links(self):
        document = self.document()
        self.assertEqual(validate(document), [])
        output = render(document, "G")
        self.assertIn("0-goal/1-1-a.md", output["0-goal.md"])
        self.assertIn("1-1-a.md#A1", output["0-goal/2-2-b.md"])

    def test_each_state_requires_a_nonempty_closed_fence(self):
        invalid = [None, {}, [], "Plain prose", "Use `inline code`", "```text\nunclosed",
                   "```text\n  \n```", "```text\n```\nprose\n```", "````text\nvalue\n```",
                   "```text\nvalue\n~~~", "    ```text\n    value\n    ```"]
        valid = ["Before.\n\n```text\nA -> B\n```", "~~~json\n{}\n~~~",
                 "````markdown\n```text\nexample\n```\n````",
                 "```bash\necho hello\n````", "```console\r\n$ echo hello\r\nhello\r\n```"]
        for node_id in ("G", "A", "A1"):
            for field in ("current_state", "expected_result_state"):
                for value in invalid + valid:
                    with self.subTest(node=node_id, field=field, value=value):
                        document = self.document()
                        document["nodes"][node_id][field] = value
                        errors = validate(document)
                        if value in invalid:
                            self.assertTrue(any(f"nodes.{node_id}.{field}" in error and "fenced code block" in error for error in errors))
                        else:
                            self.assertEqual(errors, [])

    def test_state_fences_stay_inside_labeled_markdown_fields(self):
        document = self.document()
        output = render(document, "G")
        for node_id, filename in (("G", "0-goal.md"), ("A", "0-goal/1-1-a.md"), ("A1", "0-goal/1-1-a.md")):
            for field, label in (("current_state", "Current state"), ("expected_result_state", "Expected result state")):
                value = document["nodes"][node_id][field]
                expected = f"- {label}:\n\n" + "\n".join("  " + line if line else "" for line in value.splitlines())
                self.assertIn(expected, output[filename])

    def test_dependency_cycle_is_rejected(self):
        document = self.document()
        document["edges"]["depends_on"].append({"from": "A1", "to": "B"})
        document["edges"]["depends_on"].append({"from": "B", "to": "A1"})
        self.assertTrue(any("cycle" in error for error in validate(document)))


if __name__ == "__main__":
    unittest.main()
