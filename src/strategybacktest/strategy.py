"""Strategy Class"""

from abc import ABC, abstractmethod
from typing import Dict

import pandas as pd


class Strategy(ABC):
    """
    Trading strategy abstract class.

    Args:
        **kwargs: Arguments that the strategy might need.
    """

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __call__(self, ts: pd.Timestamp) -> Dict[str, float]:
        """
        Rebalance portfolio according to predetermined weights for each new
        timestamp.

        Args:
            ts: Timestamp for rebalance.

        Returns:
            Dictionary of target weights.
        """
        pass
