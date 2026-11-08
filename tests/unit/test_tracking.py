from inboxgent.tracking import git_sha


def test_git_sha_is_hex_or_unknown() -> None:
    sha = git_sha()
    assert sha == "unknown" or len(sha) == 40
