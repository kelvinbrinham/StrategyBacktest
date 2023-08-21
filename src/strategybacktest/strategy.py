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


class DummyStrategy(Strategy):
    """
    Dummy strategy class which takes predetermined weights from a dataframe.

    Args:
        weights_df: Time-series dataframe of weights for each asset.
    """

    def __init__(self, weights_df: pd.DataFrame) -> None:
        self.weights_df = weights_df
        self._current_weights = {}

    def __call__(self, ts: pd.Timestamp, **kwargs) -> Dict[str, float]:
        """
        Rebalance portfolio according to predetermined weights for each new
        timestamp.

        Args:
            ts: Timestamp for rebalance.

        Returns:
            Dictionary of target weights for each ticker.
        """
        if ts in self.weights_df.index:
            self._current_weights = self.weights_df.loc[ts].to_dict()

        return self._current_weights
