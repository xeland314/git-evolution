from evolution_context import EvolutionContext
from handler import Handler


class MetricsAccumulatorHandler(Handler):
    """Handler responsible for calculating cumulative metrics across time."""

    def process(self, context: EvolutionContext) -> None:
        """Computes the continuous chronological growth matrix for each extension.

        Args:
            context: The state data passed through the pipeline.
        """
        if not context.dates_set:
            print("Warning: No Git tracking records found.")
            return

        print("[3/5] Computing cumulative time series...")
        context.sorted_dates = sorted(list(context.dates_set))

        for ext in sorted(context.data_by_ext.keys()):
            ext_data = context.data_by_ext[ext]
            cumulative_list = []
            running_sum = 0

            for date in context.sorted_dates:
                running_sum += ext_data.get(date, 0)
                cumulative_list.append(max(0, running_sum))

            context.cumulative_series[ext] = cumulative_list
