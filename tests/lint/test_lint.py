import os
import pathlib

import gitlab.exceptions
import pytest
from dotmap import DotMap
import gitlab.v4.objects

from gitlab_ci_lint.exceptions import GitOriginParseError, BatchLintError
from gitlab_ci_lint.utils import get_gitlab_project, lint_gitlab_ci, batch_lint_files

FIXTURE_DIR = pathlib.Path(__file__).parent.resolve()


def test_ok_project():
    repo_mock = DotMap()
    repo_mock.remotes["origin"].url = "git@gitlab.com:gitlab-com/www-gitlab-com.git"
    project = get_gitlab_project(repo_mock, "test-token-string")
    assert type(project) == gitlab.v4.objects.Project


def test_bad_project():
    repo_mock = DotMap()
    repo_mock.remotes["origin"].url = "ftp@google.com"
    with pytest.raises(GitOriginParseError):
        get_gitlab_project(repo_mock, "test-token-string")


def test_lint(mocker, gitlab_ci_valid):
    project_mock = mocker.Mock()
    project_mock.ci_lint.validate.return_value = True
    lint_gitlab_ci(project_mock, gitlab_ci_valid)
    project_mock.ci_lint.validate.assert_called_once()


@pytest.mark.datafiles(FIXTURE_DIR / "test_files")
def test_lint_batch_oserror(datafiles, mocker):
    p = mocker.patch(
        "gitlab_ci_lint.utils.lint_gitlab_ci",
        side_effect=OSError(),
    )
    file = datafiles / "./sample.yml"
    with pytest.raises(BatchLintError) as e:
        batch_lint_files(None, [file])
    p.assert_called_once()


@pytest.mark.datafiles(FIXTURE_DIR / "test_files")
def test_lint_batch(datafiles, mocker):
    lp = mocker.patch("gitlab_ci_lint.utils.lint_gitlab_ci", return_value=True)
    file = datafiles / "./sample.yml"
    batch_lint_files(None, [file])
    lp.assert_called_once()
