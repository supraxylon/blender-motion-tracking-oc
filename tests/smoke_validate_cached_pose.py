"""Smoke checks for cached pose JSON import assets.

This script intentionally uses only the Python standard library.
"""

from __future__ import annotations

import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path


REQUIRED_FILES = (
    "schemas/tracking_result.schema.json",
    "examples/sample_tracking_result.json",
    "tools/validate_tracking_json.py",
    "src/blender_pose_tracker/__init__.py",
    "src/blender_pose_tracker/importer.py",
)

ADDON_FILES = (
    "src/blender_pose_tracker/__init__.py",
    "src/blender_pose_tracker/importer.py",
)


def find_repo_root(start: Path) -> Path:
    for path in (start, *start.parents):
        if (path / ".git").exists() and (path / "README.md").exists():
            return path
    raise RuntimeError("Could not find repo root from smoke script location")


def main() -> int:
    repo_root = find_repo_root(Path(__file__).resolve())
    print(f"Repo root: {repo_root}")

    missing = [path for path in REQUIRED_FILES if not (repo_root / path).is_file()]
    if missing:
        print("FAIL: missing required files")
        for path in missing:
            print(f"  - {path}")
        return 1

    print("PASS: required files exist")

    sample_json = repo_root / "examples/sample_tracking_result.json"
    validator = repo_root / "tools/validate_tracking_json.py"
    result = subprocess.run(
        [sys.executable, "-S", str(validator), str(sample_json)],
        cwd=repo_root,
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        print("FAIL: sample tracking JSON validation failed")
        return result.returncode

    print("PASS: sample tracking JSON validates")

    with tempfile.TemporaryDirectory(prefix="cached_pose_smoke_") as tmp_dir:
        for rel_path in ADDON_FILES:
            pyc_path = Path(tmp_dir) / (Path(rel_path).name + "c")
            py_compile.compile(str(repo_root / rel_path), cfile=str(pyc_path), doraise=True)
            print(f"PASS: compiled {rel_path}")

    green_field = repo_root / "test_data/green_field.mp4"
    if green_field.exists():
        print("NOTE: test_data/green_field.mp4 exists; smoke check does not process video.")
    else:
        print("NOTE: test_data/green_field.mp4 is not present.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
