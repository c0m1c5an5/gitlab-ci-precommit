import pathlib

import pytest

from gitlab_ci_fmt.cli import cli

FIXTURE_DIR = pathlib.Path(__file__).parent.resolve()


def test_cli_no_parameters():
    with pytest.raises(SystemExit) as e:
        cli([])
    assert e.value.code == 2


def test_cli(mocker):
    print(type(mocker))
    p = mocker.patch("gitlab_ci_fmt.cli.batch_format_files", return_value=True)
    cli(["./testfile1", "./testfile2"])
    p.assert_called_once()
