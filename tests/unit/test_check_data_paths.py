import importlib.util
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "check_data_paths", Path(__file__).parents[2] / "scripts" / "check_data_paths.py"
)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_blocks_raw_data_path() -> None:
    assert module.check(["data/raw/maildir/x"])


def test_blocks_windows_style_path() -> None:
    assert module.check(["data\interim\a.parquet"])


def test_allows_labeled_and_code(tmp_path: Path) -> None:
    assert module.check(["data/labeled/gold.csv", "src/inboxgent/config.py"]) == []


def test_blocks_large_file(tmp_path: Path) -> None:
    big = tmp_path / "big.bin"
    big.write_bytes(b"0" * (module.MAX_BYTES + 1))
    assert module.check([str(big)])
