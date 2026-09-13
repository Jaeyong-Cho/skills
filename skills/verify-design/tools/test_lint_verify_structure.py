#!/usr/bin/env python3
import os
import subprocess
import tempfile
from pathlib import Path

TOOL = Path(__file__).with_name("lint-verify-structure")
DOMAINS = ("prepare", "ut", "it", "e2e", "style", "archi")


def make_project(root: Path) -> None:
    verify = root / "verify"
    verify.mkdir()
    (verify / "index.md").write_text(
        "# Verification\n\n" + "\n".join(
            f"- [{domain}/](./{domain}/) — {domain} checks." for domain in DOMAINS
        ) + "\n- [run.sh](./run.sh) — Runs verification.\n"
    )
    (verify / "run.sh").write_text("#!/bin/sh\nexit 0\n")
    for domain in DOMAINS:
        directory = verify / domain
        directory.mkdir()
        (directory / "index.md").write_text(
            f"# {domain}\n\n- [run.sh](./run.sh) — Runs {domain}.\n"
        )
        (directory / "run.sh").write_text("#!/bin/sh\nexit 0\n")
        os.chmod(directory / "run.sh", 0o755)
    os.chmod(verify / "run.sh", 0o755)


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(TOOL), str(root)], text=True, capture_output=True)


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        make_project(root)
        result = run(root)
        assert result.returncode == 0, result.stdout + result.stderr
        (root / "verify" / "prepare" / "run.sh").unlink()
        result = run(root)
        assert result.returncode != 0
        assert "V-RUN-002" in result.stdout
        assert "verify/prepare/run.sh" in result.stdout


if __name__ == "__main__":
    main()
