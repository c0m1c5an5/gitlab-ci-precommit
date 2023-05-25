import subprocess

from gitlab_ci_fmt.exceptions import (
    BatchFmtError,
    GitlabCiFmtException,
    ResultMismatchError,
)


def test_base_fmt_exception() -> None:
    e = GitlabCiFmtException("test_base_fmt_exception")
    assert e.message == "test_base_fmt_exception"


def test_result_mismatch_error() -> None:
    e = ResultMismatchError()
    assert e.message == "An error occurred while validating format result."


def test_batch_fmt_error() -> None:
    se = subprocess.CalledProcessError(
        stderr="test_batch_lint_error_subprocess".encode(), cmd="test", returncode=1
    )
    ee = Exception("test_batch_lint_error_exception")
    errors = {"/test1.txt": se, "/test2.txt": ee}
    e = BatchFmtError(errors)
    print(e.message)
    assert (
        "File: /test1.txt\nCalledProcessError: test_batch_lint_error_subprocess"
        in e.message
    )
    assert "File: /test2.txt\nException: test_batch_lint_error_exception" in e.message
