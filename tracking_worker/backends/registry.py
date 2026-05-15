"""Small backend registry for external pose tracking."""

from __future__ import annotations

from typing import Any, Callable


class BackendUnavailableError(RuntimeError):
    """Raised when a backend is known but cannot run in this environment."""


BackendFn = Callable[..., dict[str, Any]]


def _fixture() -> BackendFn:
    from tracking_worker.backends.fixture import generate

    return generate


def _rtmpose() -> BackendFn:
    from tracking_worker.backends.rtmpose import generate

    return generate


_BACKENDS: dict[str, Callable[[], BackendFn]] = {
    "fixture": _fixture,
    "rtmpose": _rtmpose,
}


def available_backends() -> tuple[str, ...]:
    return tuple(_BACKENDS.keys())


def run_backend(name: str, *, source: str) -> dict[str, Any]:
    try:
        factory = _BACKENDS[name]
    except KeyError as exc:
        raise BackendUnavailableError(f"Unknown backend: {name}") from exc
    return factory()(source=source)
