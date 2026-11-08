from hypothesis import given
from hypothesis import strategies as st

from inboxgent.cleaning import clean

text_st = st.text(alphabet=st.characters(blacklist_categories=("Cs",)), max_size=300) | st.lists(
    st.sampled_from(
        [
            "hello",
            "> quoted",
            "--",
            "-----Original Message-----",
            "On Mon, 1 Jan 2001, X wrote:",
            "",
            "  ",
        ]
    ),
    max_size=12,
).map("\n".join)


@given(text_st)
def test_idempotent(text: str) -> None:
    once = clean(text).text
    assert clean(once).text == once


@given(text_st)
def test_no_growth_after_normalization(text: str) -> None:
    out = clean(text).text
    # NFKC may expand a few compatibility characters; allow only that bounded growth.
    assert len(out) <= len(text) * 4 + 4


@given(text_st)
def test_never_raises_and_lineage_nonnegative(text: str) -> None:
    r = clean(text)
    assert all(v >= 0 for v in r.chars_removed_by_step.values())
