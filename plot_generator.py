from datetime import datetime, timedelta

import plotly.graph_objects as go

from evolution_context import EvolutionContext
from handler import Handler

DATE_FORMAT = "%Y-%m-%d"


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
                    mode="lines+markers",
                    stackgroup="one",
                    name=f".{ext}",
                    fill="tonexty",
                    marker={"size": 6},
                )
            )

        fig.update_layout(
            title="Code Evolution by Language",
            xaxis_title="Date",
            yaxis_title="Lines of Code",
            hovermode="x unified",
            template="plotly_dark",
        )

        self._fix_xaxis_range(fig, context.sorted_dates)

        context.plotly_div = fig.to_html(full_html=False, include_plotlyjs="cdn")

    @staticmethod
    def _fix_xaxis_range(fig: go.Figure, sorted_dates: list) -> None:
        """Forces an explicit, padded date range on the X axis.

        Plotly's autorange for a date axis derives its padding from the
        span between the first and last point. When that span is tiny
        (e.g. only 1-2 commits a day apart, or all commits on one day),
        the computed padding collapses to a sub-second window and the
        plotted data ends up outside the visible range entirely, even
        though it was drawn correctly. Setting the range explicitly with
        a sane minimum padding avoids that edge case for any dataset size.

        Args:
            fig: The Plotly figure whose X axis range will be set.
            sorted_dates: Chronologically sorted "YYYY-MM-DD" date strings.
        """
        if not sorted_dates:
            return

        first_date = datetime.strptime(sorted_dates[0], DATE_FORMAT).astimezone()
        last_date = datetime.strptime(sorted_dates[-1], DATE_FORMAT).astimezone()
        span_days = (last_date - first_date).days

        # At least half a day of padding on each side, growing with the
        # span so wide ranges still get proportionally sensible margins.
        padding = timedelta(days=max(0.5, span_days * 0.05))

        fig.update_xaxes(
            type="date",
            range=[
                (first_date - padding).isoformat(),
                (last_date + padding).isoformat(),
            ],
        )
