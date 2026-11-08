"""Command line entry point."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from inboxgent import __version__
from inboxgent.config import load_settings
from inboxgent.logging import setup_logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="inboxgent", description="InBoxGent pipeline CLI")
    parser.add_argument("--version", action="version", version=f"inboxgent {__version__}")
    parser.add_argument("--config", type=Path, default=None, help="path to a YAML config file")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("show-config", help="print the effective configuration (secrets masked)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = load_settings(args.config)
    setup_logging(settings.logging.level)
    if args.command == "show-config":
        print(settings.model_dump_json(indent=2))  # noqa: T201
    return 0
