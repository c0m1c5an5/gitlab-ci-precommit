import subprocess

from gitlab_ci_lint.exceptions import (
    GitlabCiLintException,
    GitOriginParseError,
    GitTokenMissing,
    BatchLintError,
)


def test_base_lint_exception() -> None:
    e = GitlabCiLintException("test_base_lint_exception")
    assert e.message == "test_base_lint_exception"


def test_git_token_missing() -> None:
    e = GitTokenMissing()
    assert e.message == "GitLab personal access token is missing."


def test_git_origin_parse_error() -> None:
    e = GitOriginParseError("https://example.com")
    assert (
        e.message
        == "An error occurred while parsing git origin url. Origin url: https://example.com"
    )


def test_batch_lint_error() -> None:
    se = subprocess.CalledProcessError(
        stderr="test_batch_lint_error_subprocess".encode(), cmd="test", returncode=1
    )
    ee = Exception("test_batch_lint_error_exception")
    errors = {"/test1.txt": se, "/test2.txt": ee}
    e = BatchLintError(errors)
    print(e.message)
    assert (
        "File: /test1.txt\nCalledProcessError: test_batch_lint_error_subprocess"
        in e.message
    )
    assert "File: /test2.txt\nException: test_batch_lint_error_exception" in e.message
