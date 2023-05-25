import pathlib

import git
import gitlab
import gitlab.exceptions
import gitlab.v4.objects
import giturlparse

from gitlab_ci_lint.exceptions import BatchLintError, GitOriginParseError


def get_gitlab_project(git_repo: git.Repo, token: str) -> gitlab.v4.objects.Project:
    origin = git_repo.remotes["origin"]
    parsed_url = giturlparse.parse(origin.url)
    if parsed_url.valid:
        project_path = parsed_url.pathname.removeprefix("/").removesuffix(".git")
        gitlab_host = "https://" + parsed_url.host
        gl = gitlab.Gitlab(gitlab_host, private_token=token)
        return gl.projects.get(project_path, lazy=True)
    else:
        raise GitOriginParseError(origin.url)


def lint_gitlab_ci(project: gitlab.v4.objects.Project, yml: str) -> None:
    project.ci_lint.validate({"content": yml})


def batch_lint_files(
    project: gitlab.v4.objects.Project, files: list[pathlib.Path]
) -> None:
    errors: dict[str, Exception] = dict()

    for file_path in files:
        try:
            file_path = file_path.resolve()
            with file_path.open("r") as src_file:
                yml = src_file.read()

            lint_gitlab_ci(project, yml)
        except (OSError, gitlab.exceptions.GitlabError) as e:
            errors[str(file_path)] = e
            continue

    if errors:
        raise BatchLintError(errors)
