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
            "current_state": "c", "expected_result_state": "e",
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
                    "current_state": "c", "expected_result_state": "e",
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

    def test_dependency_cycle_is_rejected(self):
        document = self.document()
        document["edges"]["depends_on"].append({"from": "A1", "to": "B"})
        document["edges"]["depends_on"].append({"from": "B", "to": "A1"})
        self.assertTrue(any("cycle" in error for error in validate(document)))


if __name__ == "__main__":
    unittest.main()
