import subprocess


class GitlabCiLintException(Exception):
    message: str

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GitTokenMissing(GitlabCiLintException):
    def __init__(self):
        self.message = "GitLab personal access token is missing."
        self.add_note(
            "Set the access token with GCL_PERSONAL_ACCESS_TOKEN environment variable. Alternatively use -t flag."
        )
        super().__init__(self.message)


class GitOriginParseError(GitlabCiLintException):
    origin_url: str

    def __init__(self, origin_url: str):
        self.origin_url = origin_url
        self.message = f"An error occurred while parsing git origin url. Origin url: {self.origin_url}"
        self.add_note("Git origin url is not a valid url.")
        super().__init__(self.message)


class BatchLintError(GitlabCiLintException):
    errors: dict[str, Exception]

    def __init__(self, errors: dict[str, Exception] = {}):
        self.errors = errors
        self.message = "Batch lint failed.\n"
        for file, error in self.errors.items():
            self.message += f"File: {file}\n"
            if type(error) is subprocess.CalledProcessError:
                self.message += f"{type(error).__name__}: {error.stderr.decode()}\n"
            else:
                self.message += f"{type(error).__name__}: {error}\n"
        self.message = self.message.rstrip()
        super().__init__(self.message)
