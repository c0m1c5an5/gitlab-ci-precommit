import argparse
import os
import pathlib
import sys

import git

from gitlab_ci_lint.exceptions import GitTokenMissing
from gitlab_ci_lint.utils import batch_lint_files, get_gitlab_project


def cli(argv: list[str] = sys.argv[1:]) -> None:
    sys.tracebacklimit = 0
    parser = argparse.ArgumentParser(prog=__package__)
    parser.add_argument("files", nargs="+", type=pathlib.Path, help="Files to lint.")
    parser.add_argument(
        "-t", "--token", type=str, required=False, help="GitLab personal access token."
    )
    args = parser.parse_args(argv)

    if args.token:
        token = args.token
    elif os.environ.get("GCL_PERSONAL_ACCESS_TOKEN"):
        token = os.environ.get("GCL_PERSONAL_ACCESS_TOKEN")
    else:
        raise GitTokenMissing()

    repo = git.Repo(".", search_parent_directories=True)
    project = get_gitlab_project(repo, token)

    batch_lint_files(project, args.files)
