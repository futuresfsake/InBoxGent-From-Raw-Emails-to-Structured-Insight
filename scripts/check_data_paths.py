"""Pre-commit blocker: refuse staged files under ignored data zones or above a size limit."""

from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

BLOCKED_PREFIXES = ("data/raw/", "data/interim/", "data/features/", "data/outputs/", "mlruns/")
MAX_BYTES = 1_000_000


def check(paths: Sequence[str]) -> list[str]:
    problems: list[str] = []
    for name in paths:
        norm = name.replace("\\", "/")
        if norm.startswith(BLOCKED_PREFIXES):
            problems.append(f"{name}: path is a git-ignored data zone")
            continue
        path = Path(name)
        if path.is_file() and path.stat().st_size > MAX_BYTES:
            problems.append(f"{name}: larger than {MAX_BYTES} bytes")
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    problems = check(sys.argv[1:] if argv is None else argv)
    for problem in problems:
        print(problem, file=sys.stderr)  # noqa: T201
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
