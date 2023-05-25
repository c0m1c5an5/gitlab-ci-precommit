import filecmp
import pathlib

import pytest

from gitlab_ci_fmt.exceptions import ResultMismatchError, BatchFmtError
from gitlab_ci_fmt.utils import (
    batch_format_files,
    format_gitlab_ci,
    yq_compare,
    yq_sort_keys,
)

FIXTURE_DIR = pathlib.Path(__file__).parent.resolve()


def test_yq_sort_keys(simple_yml_unsorted, simple_yml_sorted) -> None:
    result = yq_sort_keys(simple_yml_unsorted)
    assert result == simple_yml_sorted


def test_yq_ok_compare(simple_yml_unsorted, simple_yml_sorted) -> None:
    assert yq_compare(simple_yml_unsorted, simple_yml_sorted)


def test_yq_bad_compare(simple_yml_unsorted, gitlab_ci_unformatted) -> None:
    assert not yq_compare(simple_yml_unsorted, gitlab_ci_unformatted)


def test_format_gitlab_ci(gitlab_ci_unformatted, gitlab_ci_formatted) -> None:
    assert format_gitlab_ci(gitlab_ci_unformatted) == gitlab_ci_formatted


def test_comparison_mismatch(mocker, gitlab_ci_unformatted) -> None:
    p = mocker.patch("gitlab_ci_fmt.utils.yq_compare", return_value=False)
    with pytest.raises(ResultMismatchError):
        format_gitlab_ci(gitlab_ci_unformatted)
    p.assert_called_once()


@pytest.mark.datafiles(FIXTURE_DIR / "test_files")
def test_fmt_batch_oserror(datafiles, mocker):
    p = mocker.patch(
        "gitlab_ci_fmt.utils.format_gitlab_ci",
        side_effect=OSError(),
    )
    file = datafiles / "./sample.yml"
    with pytest.raises(BatchFmtError) as e:
        batch_format_files([file])
    p.assert_called_once()


@pytest.mark.datafiles(FIXTURE_DIR / "test_files")
def test_fmt_batch(datafiles):
    source = datafiles / "./sample.yml"
    destination = datafiles / "./sample.yml"
    batch_format_files([source])
    assert filecmp.cmp(source, destination, shallow=False)
