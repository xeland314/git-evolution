from typing import Set

from handler import Handler
from evolution_context import EvolutionContext

# Target file extensions to analyze
TARGET_EXTENSIONS: Set[str] = {
    "jl",
    "py",
    "c",
    "cpp",
    "h",
    "php",
    "js",
    "html",
    "css",
    "astro",
    "ts",
    "tsx",
    "dart",
    "rust",
    "go",
    "rb",
    "swift",
    "kt",
    "scala",
    "lua",
    "r",
    "sql",
    "zig",
    "nim",
    "elixir",
    "clj",
    "cljs",
    "lisp",
    "fsharp",
    "ocaml",
    "haskell",
    "groovy",
    "perl",
    "vb",
    "powershell",
    "bash",
    "zsh",
    "fish",
    "makefile",
    "dockerfile",
    "yaml",
    "json",
    "xml",
    "toml",
}


class GitLogParseHandler(Handler):
    """Handler responsible for fast, non-regex extraction of lines of code."""

    def process(self, context: EvolutionContext) -> None:
        """Parses raw text data to map additions and deletions per extension/date.

        Args:
            context: The state data passed through the pipeline.
        """
        print("[2/5] Parsing lines and extensions...")
        current_date = ""

        for line in context.raw_log.splitlines():
            line = line.strip()
            if not line:
                continue

            # Strict YYYY-MM-DD date identification without regex
            if len(line) == 10 and line[4] == "-" and line[7] == "-":
                current_date = line
                context.dates_set.add(current_date)
                continue

            # Split up to 3 parts (additions, deletions, file path)
            parts = line.split(maxsplit=2)
            if len(parts) == 3:
                add_str, del_str, file_path = parts
                if add_str == "-" or del_str == "-":
                    continue

                dot_idx = file_path.rfind(".")
                if dot_idx != -1 and dot_idx < len(file_path) - 1:
                    ext = file_path[dot_idx + 1 :].lower()

                    if ext in TARGET_EXTENSIONS:
                        net_lines = int(add_str) - int(del_str)
                        context.data_by_ext[ext][current_date] += net_lines
