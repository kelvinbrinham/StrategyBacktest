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
    def __init__(self, **kwargs) -> None:
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
        weights_df: dataframe of weights for each asset
    """

    def __init__(self, weights_df: pd.DataFrame) -> None:
        self.weights_df = weights_df
        self._current_weights = {}

    def __call__(self, ts: pd.Timestamp) -> Dict[str, float]:
        """
        Rebalance portfolio according to predetermined weights for each new
        timestamp.

        Args:
            ts: Timestamp for rebalance.

        Returns:
            Dictionary of target weights.
        """
        if ts in self.weights_df.index:
            self._current_weights = self.weights_df.loc[ts].to_dict()

        return self._current_weights


class Momentum(Strategy):
    """
    Simple momentum strategy. Long the top asset and short the bottom asset.
    Monthly re-weighting.

    Args:
        weights_df: Dataframe of initial weights for each asset.
        prices_df: dataframe of prices for each asset for the new day
        (only, to avoid look ahead bias).
    """

    def __init__(
        self, weights_df: pd.DataFrame, prices_df: pd.DataFrame
    ) -> None:
        self.weights_df = weights_df
        self.prices_df = prices_df
        self._prices_record = pd.DataFrame()
        self._current_weights = {}
        self._initial = True
        self._second = True

    def __call__(self, ts: pd.Timestamp) -> Dict[str, float]:
        """
        Rebalance portfolio for each new timestamp.

        Args:
            ts: Current timestamp.

        Returns:
            Portfolio weights.
        """
        # Get new price
        new_price_df = self.prices_df.loc[ts].to_frame().T
        # Update historical prices
        self._prices_record = pd.concat([self._prices_record, new_price_df])

        if ts in self.weights_df.index:
            # print('-' * 20, ts, '-' * 20)
            # For the first two months, return the default weights.
            if self._initial or self._second:
                self._current_weights = self.weights_df.loc[ts].to_dict()

            else:
                # After the first two months, calculate the returns for each
                # asset
                month_prices = self._prices_record[
                    ts
                    - pd.DateOffset(months=2) : ts
                    - pd.DateOffset(months=1, days=1)
                ]
                returns_df = month_prices.pct_change().dropna().mean()
                winner = returns_df.idxmax()
                # loser = returns_df.idxmin()
                # self._current_weights = {winner: 0.5, loser: -0.5}
                if returns_df[winner].mean() > 0:
                    self._current_weights = {winner: 1}
                else:
                    self._current_weights = {}

            if not self._initial:
                self._second = False
            self._initial = False

        return self._current_weights
