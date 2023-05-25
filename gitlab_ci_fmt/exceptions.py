import subprocess


class GitlabCiFmtException(Exception):
    message: str

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ResultMismatchError(GitlabCiFmtException):
    def __init__(self):
        self.message = "An error occurred while validating format result."
        self.add_note("This is a bug. Please report it to the issues tab.")
        super().__init__(self.message)


class BatchFmtError(GitlabCiFmtException):
    errors: dict[str, Exception]

    def __init__(self, errors: dict[str, Exception] = {}):
        self.errors = errors
        self.message = "Batch formatting failed.\n"
        for file, error in self.errors.items():
            self.message += f"File: {file}\n"
            if type(error) is subprocess.CalledProcessError:
                self.message += f"{type(error).__name__}: {error.stderr.decode()}\n"
            else:
                self.message += f"{type(error).__name__}: {error}\n"
        self.message = self.message.rstrip()
        super().__init__(self.message)
