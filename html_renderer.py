import os
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
        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir, TEMPLATE_FILENAME)
        output_filename = OUTPUT_FILENAME

        try:
            with open(template_path, "r", encoding="utf-8") as file:
                template_content = file.read()

            final_html = template_content.replace(
                "{{ graphic_component }}", context.plotly_div
            )

            with open(output_filename, "w", encoding="utf-8") as file:
                file.write(final_html)

            print(f"Success! Output generated in target path: '{output_filename}'")

        except FileNotFoundError:
            print(
                f"Error: Missing required file asset '{TEMPLATE_FILENAME}' inside: {script_dir}"
            )
