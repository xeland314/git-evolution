from abc import ABC, abstractmethod
from typing import Optional

from evolution_context import EvolutionContext

class Handler(ABC):
    """Abstract base handler for the Chain of Responsibility pattern."""

    def __init__(self, next_handler: Optional["Handler"] = None) -> None:
        """Initializes the handler link.

        Args:
            next_handler: The next link in the execution chain.
        """
        self._next_handler: Optional[Handler] = next_handler

    def set_next(self, handler: "Handler") -> "Handler":
        """Sets the next handler in the chain dynamically.

        Args:
            handler: The next handler instance.

        Returns:
            The passed handler instance to allow chaining.
        """
        self._next_handler = handler
        return handler

    def handle(self, context: EvolutionContext) -> None:
        """Executes current processing step and forwards context down the chain.

        Args:
            context: The state data passed through the pipeline.
        """
        self.process(context)
        if self._next_handler:
            self._next_handler.handle(context)

    @abstractmethod
    def process(self, context: EvolutionContext) -> None:
        """Abstract method containing specific business logic for this step.

        Args:
            context: The state data passed through the pipeline.
        """
        pass
