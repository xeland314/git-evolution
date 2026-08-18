import os
import sys
from datetime import datetime

from evolution_context import EvolutionContext
from handler import Handler

TEMPLATE_FILENAME = "template.html"
OUTPUT_FILENAME = "git-evolution.html"


class HtmlRendererHandler(Handler):
    """Handler responsible for mixing the Plotly component inside an HTML layout."""

    def process(self, context: EvolutionContext) -> None:
        """Reads local template files and exports the fully processed layout.

        Args:
            context: The state data passed through the pipeline.
        """
        if not context.plotly_div:
            return

        print("[5/5] Injecting asset into HTML template...")
        template_path = os.path.join(self._resource_dir(), TEMPLATE_FILENAME)
        output_filename = OUTPUT_FILENAME

        try:
            with open(template_path, "r", encoding="utf-8") as file:
                template_content = file.read()

            final_html = (
                template_content.replace("{{ graphic_component }}", context.plotly_div)
                .replace("{{ repo_name }}", context.repo_name or "Repositorio")
                .replace(
                    "{{ generated_date }}",
                    datetime.now().astimezone().strftime("%d/%m/%Y %H:%M"),
                )
                .replace("{{ commit_count }}", str(context.commit_count))
            )

            with open(output_filename, "w", encoding="utf-8") as file:
                file.write(final_html)

            print(f"Success! Output generated in target path: '{output_filename}'")

        except FileNotFoundError:
            print(
                f"Error: Missing required file asset '{TEMPLATE_FILENAME}' inside: {self._resource_dir()}"
            )

    @staticmethod
    def _resource_dir() -> str:
        """Resolves the directory holding bundled assets.

        When frozen by PyInstaller (onefile mode), assets are unpacked into
        ``sys._MEIPASS`` at runtime; otherwise fall back to this file's directory.
        """
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            return meipass
        return os.path.dirname(os.path.abspath(__file__))
