.PHONY: install hooks lint format typecheck test check

install:
	pip install -e ".[dev]"

hooks:
	git config core.hooksPath .githooks

lint:
	ruff check src tests

format:
	ruff format src tests

typecheck:
	mypy

test:
	pytest --cov=inboxgent --cov-report=term-missing

check: lint typecheck test
