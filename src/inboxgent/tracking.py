"""Experiment tracking skeleton (MLflow, local file store).

MLflow is an optional dependency (``pip install -e ".[tracking]"``) imported lazily so the
core package and CI stay light. Every run records the git SHA and the data manifest hash.
"""

from __future__ import annotations

import subprocess  # nosec B404
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any

DEFAULT_TRACKING_URI = "file:./mlruns"


def git_sha() -> str:
    try:
        out = subprocess.run(  # noqa: S603  # nosec B603 B607
            ["git", "rev-parse", "HEAD"],  # noqa: S607
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return out.stdout.strip()


@contextmanager
def start_run(
    experiment: str,
    *,
    manifest_hash: str,
    params: Mapping[str, Any] | None = None,
    tracking_uri: str = DEFAULT_TRACKING_URI,
) -> Iterator[Any]:
    """Open an MLflow run tagged with git SHA and data manifest hash."""
    try:
        import mlflow
    except ImportError as exc:  # pragma: no cover - exercised only without the extra
        raise RuntimeError("mlflow is not installed; use `pip install -e .[tracking]`") from exc
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment)
    with mlflow.start_run() as run:
        mlflow.set_tags({"git_sha": git_sha(), "manifest_hash": manifest_hash})
        if params:
            mlflow.log_params(dict(params))
        yield run
