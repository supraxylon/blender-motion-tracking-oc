"""Plain-assert tests for tracking_worker with the fixture backend."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def _find_repo_root() -> Path:
    here = Path(__file__).resolve().parent
    for parent in (here, *here.parents):
        if (parent / ".git").is_dir():
            return parent
    return here.parent


REPO_ROOT = _find_repo_root()
sys.path.insert(0, str(REPO_ROOT))
_CLI_ENV = {**os.environ, "PYTHONPATH": str(REPO_ROOT)}


def _run_cli(output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-S",
            "-m",
            "tracking_worker.cli",
            "--input",
            "test_data/green_field.mp4",
            "--output",
            str(output),
            "--backend",
            "fixture",
        ],
        cwd=REPO_ROOT,
        env=_CLI_ENV,
        capture_output=True,
        text=True,
    )


def test_generate_fixture_structure() -> None:
    from tracking_worker.fixture_backend import generate_fixture

    data = generate_fixture(source="test_data/green_field.mp4")
    assert "video_meta" in data
    assert "frames" in data
    assert len(data["frames"]) == 2
    for frame in data["frames"]:
        assert "frame_index" in frame
        assert "width" in frame
        assert "height" in frame
        assert "persons" in frame
        assert len(frame["persons"]) >= 1


def test_fixture_keypoints_exactly_17() -> None:
    from tracking_worker.fixture_backend import generate_fixture

    data = generate_fixture(source="test_data/green_field.mp4")
    person = data["frames"][0]["persons"][0]
    assert len(person["keypoints"]) == 17
    for kp in person["keypoints"]:
        assert {"x", "y", "score"}.issubset(kp)
        assert 0 <= kp["x"] <= 1
        assert 0 <= kp["y"] <= 1


def test_fixture_bbox_valid() -> None:
    from tracking_worker.fixture_backend import generate_fixture

    data = generate_fixture(source="test_data/green_field.mp4")
    for frame in data["frames"]:
        for person in frame["persons"]:
            bbox = person["bbox"]
            assert bbox["x"] >= 0
            assert bbox["y"] >= 0
            assert bbox["width"] >= 0
            assert bbox["height"] >= 0


def test_validate_tracking_json_ok() -> None:
    from tracking_worker.fixture_backend import generate_fixture
    from tracking_worker.schema_io import validate_tracking_json

    data = generate_fixture(source="test_data/green_field.mp4")
    ok, errs = validate_tracking_json(data)
    assert ok, f"validation errors: {errs}"


def test_validate_missing_frames() -> None:
    from tracking_worker.schema_io import validate_tracking_json

    ok, errs = validate_tracking_json({"video_meta": {"width": 640, "height": 480}})
    assert not ok
    assert any("frames" in e for e in errs)


def test_cli_writes_output() -> None:
    with tempfile.TemporaryDirectory(prefix="worker_test_") as tmpd:
        out = Path(tmpd) / "out.json"
        result = _run_cli(out)
        assert result.returncode == 0, f"stderr:\n{result.stderr}"
        assert out.exists(), "output file was not created"
        data = json.loads(out.read_text(encoding="utf-8"))
        assert len(data["frames"]) == 2


def test_cli_validation_pass() -> None:
    with tempfile.TemporaryDirectory(prefix="worker_val_") as tmpd:
        out = Path(tmpd) / "val.json"
        result = _run_cli(out)
        assert result.returncode == 0, f"worker failed:\n{result.stderr}"

        validator = REPO_ROOT / "tools" / "validate_tracking_json.py"
        result = subprocess.run(
            [sys.executable, "-S", str(validator), str(out)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"validation failed:\n{result.stdout}\n{result.stderr}"
        assert "PASS" in result.stdout


def test_rtmpose_backend_fails_clearly_without_environment() -> None:
    with tempfile.TemporaryDirectory(prefix="worker_rtmpose_") as tmpd:
        out = Path(tmpd) / "rtmpose.json"
        result = subprocess.run(
            [
                sys.executable,
                "-S",
                "-m",
                "tracking_worker.cli",
                "--input",
                "test_data/green_field.mp4",
                "--output",
                str(out),
                "--backend",
                "rtmpose",
            ],
            cwd=REPO_ROOT,
            env=_CLI_ENV,
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "BACKEND UNAVAILABLE" in result.stderr
        assert "RTMPose backend is not installed" in result.stderr
        assert not out.exists()


def main() -> int:
    tests = [
        test_generate_fixture_structure,
        test_fixture_keypoints_exactly_17,
        test_fixture_bbox_valid,
        test_validate_tracking_json_ok,
        test_validate_missing_frames,
        test_cli_writes_output,
        test_cli_validation_pass,
        test_rtmpose_backend_fails_clearly_without_environment,
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
