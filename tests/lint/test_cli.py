import os
import pathlib

import git
import git.exc
import gitlab.exceptions
import pytest
from dotmap import DotMap

from gitlab_ci_lint.cli import cli
from gitlab_ci_lint.exceptions import (
    BatchLintError,
    GitOriginParseError,
    GitTokenMissing,
)

FIXTURE_DIR = pathlib.Path(__file__).parent.resolve()


def test_no_parameters() -> None:
    with pytest.raises(SystemExit) as e:
        cli([])
    assert e.value.code == 2


def test_no_token(mocker) -> None:
    mocker.patch.dict(os.environ, {"GCL_PERSONAL_ACCESS_TOKEN": ""}, clear=True)
    with pytest.raises(GitTokenMissing):
        cli(["./ghost_file_not_exists"])


def test_token_env(tmpdir, mocker) -> None:
    os.chdir(tmpdir)
    mocker.patch.dict(
        os.environ, {"GCL_PERSONAL_ACCESS_TOKEN": "test-token-string"}, clear=True
    )
    with pytest.raises(git.exc.InvalidGitRepositoryError):
        cli(["./ghost_file_not_exists"])


def test_token_parameter(tmpdir) -> None:
    os.chdir(tmpdir)
    with pytest.raises(git.exc.InvalidGitRepositoryError):
        cli(["-t", "test-token-string", "./ghost_file_not_exists"])


@pytest.mark.datafiles(FIXTURE_DIR / "test_files")
def test_bad_gitlab_origin(datafiles, mocker):
    repo_mock = DotMap()
    repo_mock.remotes["origin"].url = ":\\invalid@url"
    p = mocker.patch("gitlab_ci_lint.cli.git.Repo", return_value=repo_mock)

    file = str(datafiles / "./sample.yml")
    with pytest.raises(GitOriginParseError) as e:
        cli(["-t", "test-token-string", file])

    p.assert_called_once()


def test_cli(mocker):
    repo_mock = DotMap()
    repo_mock.remotes[
        "origin"
    ].url = "git@gitlab.com:gitlab-com/gl-infra/cicd-and-enablement/gitlab.git"

    project_mock_sentinel = object()

    rp = mocker.patch("gitlab_ci_lint.cli.git.Repo", return_value=True)
    lp = mocker.patch(
        "gitlab_ci_lint.cli.get_gitlab_project", return_value=project_mock_sentinel
    )
    p = mocker.patch("gitlab_ci_lint.cli.batch_lint_files", return_value=True)

    file_a = pathlib.Path("./file_a")
    file_b = pathlib.Path("./file_b")

    cli(["-t", "test-token-string", str(file_a), str(file_b)])

    _, files_parameter = p.call_args.args
    assert files_parameter == [file_a, file_b]
    lp.assert_called_once()
    rp.assert_called_once()
