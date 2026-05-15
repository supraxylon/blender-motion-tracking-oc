"""CLI entry-point for the tracking worker."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from tracking_worker.backends import BackendUnavailableError, available_backends, run_backend
from tracking_worker.schema_io import validate_tracking_json, write_tracking_result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tracking_worker",
        description="Pose tracking worker (COCO-17).",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input video path (used as source metadata).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output JSON path.",
    )
    parser.add_argument(
        "--backend",
        required=True,
        choices=available_backends(),
        help="Backend to run (e.g. fixture).",
    )
    args = parser.parse_args(argv)

    source = str(Path(args.input).resolve())
    print(f"[worker] input:  {source}")
    print(f"[worker] output: {args.output}")
    print(f"[worker] backend:{args.backend}")

    try:
        data = run_backend(args.backend, source=source)
    except BackendUnavailableError as exc:
        print(f"[worker] BACKEND UNAVAILABLE: {exc}", file=sys.stderr)
        return 1

    ok, errs = validate_tracking_json(data)
    if not ok:
        print("[worker] VALIDATION FAILED before write:", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 1

    write_tracking_result(data, args.output)
    print(f"[worker] wrote {args.output}  ({len(data['frames'])} frames, {sum(len(f['persons']) for f in data['frames'])} persons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
