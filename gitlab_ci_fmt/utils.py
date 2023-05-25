#!/usr/bin/env python3

import pathlib
import subprocess

from gitlab_ci_fmt.exceptions import BatchFmtError, ResultMismatchError


def yq_sort_keys(yml: str) -> str:
    return subprocess.run(
        ["yq", "-P", "sort_keys(..)"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        input=yml.encode(),
        check=True,
    ).stdout.decode()


def yq_compare(src: str, dst: str) -> bool:
    return yq_sort_keys(src) == yq_sort_keys(dst)


def yq_order_top_keys(yml: str) -> str:
    return subprocess.run(
        [
            "yq",
            '. |= pick(([ "workflow", "stages", "variables", "include", "default"] + keys) | unique)',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        input=yml.encode(),
        check=True,
    ).stdout.decode()


def yq_order_job_keys(yml: str) -> str:
    return subprocess.run(
        [
            "yq",
            '.[] |= (select(tag == "!!map") | pick(([ "extends", "stage", "tags", "image", "services", "only", "except", "rules", "when", "dependencies", "secrets", "needs", "artifacts", "coverage", "dast_configuration", "pages", "environment", "release", "trigger", "retry", "timeout", "parallel", "allow_failure", "interruptible", "resource_group", "variables", "inherit", "cache", "before_script", "script", "after_script"] + keys) | unique))',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        input=yml.encode(),
        check=True,
    ).stdout.decode()


def format_gitlab_ci(yml: str) -> str:
    result = yq_order_top_keys(yml)
    result = yq_order_job_keys(result)

    if not yq_compare(yml, result):
        raise ResultMismatchError()

    return result


def batch_format_files(files: list[pathlib.Path]) -> None:
    errors: dict[str, Exception] = dict()

    for file_path in files:
        try:
            file_path = file_path.resolve()

            with file_path.open("r") as f:
                source = f.read()

            result = format_gitlab_ci(source)

            if result != source:
                with file_path.open("w") as f:
                    f.write(result)

        except (subprocess.CalledProcessError, OSError, ResultMismatchError) as e:
            errors[str(file_path)] = e
            continue

    if errors:
        raise BatchFmtError(errors)
