from collections import defaultdict


class EvolutionContext:
    """State context passed through the Chain of Responsibility pipeline."""

    def __init__(self) -> None:
        """Initializes the context tracking variables."""
        self.raw_log: str = ""
        self.repo_name: str = ""
        self.commit_count: int = 0
        self.dates_set: set[str] = set()
        self.sorted_dates: list[str] = []
        self.data_by_ext: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.cumulative_series: dict[str, list[int]] = {}
        self.plotly_div: str = ""
