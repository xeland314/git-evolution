import plotly.graph_objects as go

from evolution_context import EvolutionContext
from handler import Handler


class PlotGeneratorHandler(Handler):
    """Handler responsible for preparing the Plotly Figure data structure."""

    def process(self, context: EvolutionContext) -> None:
        """Builds interactive stacked area charts from computed metrics.

        Args:
            context: The state data passed through the pipeline.
        """
        if not context.cumulative_series:
            return

        print("[4/5] Generating Plotly configuration...")
        fig = go.Figure()

        for ext, series in context.cumulative_series.items():
            fig.add_trace(
                go.Scatter(
                    x=context.sorted_dates,
                    y=series,
                    mode="lines",
                    stackgroup="one",
                    name=f".{ext}",
                    fill="tonexty",
                )
            )

        fig.update_layout(
            title="Code Evolution by Language",
            xaxis_title="Date",
            yaxis_title="Lines of Code",
            hovermode="x unified",
            template="plotly_dark",
        )

        context.plotly_div = fig.to_html(full_html=False, include_plotlyjs="cdn")
