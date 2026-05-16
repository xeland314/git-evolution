from collections import defaultdict
from typing import Dict, List, Set

class EvolutionContext:
    """State context passed through the Chain of Responsibility pipeline."""

    def __init__(self) -> None:
        """Initializes the context tracking variables."""
        self.raw_log: str = ""
        self.dates_set: Set[str] = set()
        self.sorted_dates: List[str] = []
        self.data_by_ext: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.cumulative_series: Dict[str, List[int]] = {}
        self.plotly_div: str = ""
