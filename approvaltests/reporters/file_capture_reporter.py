import os
from typing import Callable

from approvaltests import Reporter
from approvaltests.utilities.os_utilities import run_command


def is_git_registration_needed() -> bool:
    return os.environ.get("GITHUB_ACTIONS") is not None


def run(*args: str) -> None:
    run_command(list(args))


class FileCaptureReporter(Reporter):
    def __init__(
        self,
        message: str = "*** adding received file via FileCaptureReporter for further inspection",
        is_git_registration_needed: Callable[[], bool] = is_git_registration_needed,
    ):
        self.message = message
        self.is_git_registration_needed = is_git_registration_needed

    def report(self, received_path: str, approved_path: str) -> bool:
        if self.is_git_registration_needed():
            run("git", "config", "--local", "user.email", "action@github.com")
            run("git", "config", "--local", "user.name", "githubAction")
        run("git", "add", "--force", received_path)
        run("git", "commit", "-m", "'" + self.message + "'")
        run("git", "push")
        return True
