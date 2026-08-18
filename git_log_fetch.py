import os
import subprocess

from evolution_context import EvolutionContext
from handler import Handler


class GitLogFetchHandler(Handler):
    """Handler responsible for extracting raw numstat information from Git logs."""

    def process(self, context: EvolutionContext) -> None:
        """Executes subprocesses to gather git log history and repo metadata.

        Args:
            context: The state data passed through the pipeline.
        """
        print("[1/5] Fetching Git log history...")
        result = subprocess.run(
            ["git", "log", "--pretty=format:%as", "--numstat"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        context.raw_log = result.stdout
        context.repo_name = self._resolve_repo_name()
        context.commit_count = self._count_commits()

    def _resolve_repo_name(self) -> str:
        """Determines a human-readable repository name.

        Falls back to the current directory name if `git rev-parse` fails.
        """
        try:
            toplevel = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            ).stdout.strip()
            return os.path.basename(toplevel) or os.path.basename(os.getcwd())
        except (subprocess.CalledProcessError, FileNotFoundError):
            return os.path.basename(os.getcwd())

    def _count_commits(self) -> int:
        """Counts the total number of commits on the current branch."""
        try:
            count_str = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            ).stdout.strip()
            return int(count_str) if count_str.isdigit() else 0
        except (subprocess.CalledProcessError, FileNotFoundError):
            return 0
