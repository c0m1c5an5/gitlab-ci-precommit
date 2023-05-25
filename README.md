# Usage
Usage in `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/c0m1c5an5/gitlab-ci-precommit
  rev: 1.0.0
  hooks:
    - id: gitlab-ci-lint
    - id: gitlab-ci-fmt
```

# Issues and proposals

Feel free to create an issue, report a bug or suggest improvements in the "Issues" section.


# gitlab-ci-lint
Use gitlab api to lint gitlab-ci files.

Requirements:
- [python-gitlab](https://python-gitlab.readthedocs.io/en/stable)
- [GitPython](https://github.com/gitpython-developers/GitPython)
- [giturlparse](https://github.com/nephila/giturlparse)

# gitlab-ci-fmt
Ensure strict ordering of keywords in gitlab-ci configuration file.

Requirements:
- [yq](https://github.com/mikefarah/yq)
