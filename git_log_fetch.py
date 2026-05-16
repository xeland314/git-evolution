import subprocess

from evolution_context import EvolutionContext
from handler import Handler


class GitLogFetchHandler(Handler):
    """Handler responsible for extracting raw numstat information from Git logs."""

    def process(self, context: EvolutionContext) -> None:
        """Executes a subprocess to gather the git log history.

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
