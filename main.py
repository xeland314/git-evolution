#!/usr/bin/env uv run
# /// script
# dependencies = [
#   "plotly",
# ]
# ///
from evolution_context import EvolutionContext
from git_log_fetch import GitLogFetchHandler
from git_log_parse import GitLogParseHandler
from metrics import MetricsAccumulatorHandler
from plot_generator import PlotGeneratorHandler
from html_renderer import HtmlRendererHandler


def main() -> None:
    """Entry point orchestration running the Chain of Responsibility pipeline."""
    # Define chain instances
    fetch_step = GitLogFetchHandler()
    parse_step = GitLogParseHandler()
    metrics_step = MetricsAccumulatorHandler()
    plot_step = PlotGeneratorHandler()
    render_step = HtmlRendererHandler()

    # Form the sequential pipeline chain
    fetch_step.set_next(parse_step).set_next(metrics_step).set_next(plot_step).set_next(
        render_step
    )

    # Initialize data carrier and run
    context = EvolutionContext()
    fetch_step.handle(context)


if __name__ == "__main__":
    main()
