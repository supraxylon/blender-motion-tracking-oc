"""Fixture backend adapter."""

from __future__ import annotations

from typing import Any

from tracking_worker.fixture_backend import generate_fixture


def generate(source: str) -> dict[str, Any]:
    return generate_fixture(source=source)
