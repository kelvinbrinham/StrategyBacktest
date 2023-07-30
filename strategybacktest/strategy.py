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
        weights_df: Time-series dataframe of weights for each asset.
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
            Dictionary of target weights for each ticker.
        """
        if ts in self.weights_df.index:
            self._current_weights = self.weights_df.loc[ts].to_dict()

        return self._current_weights


class Momentum(Strategy):
    """
    Simple momentum strategy.

    Assets are ranked based on mean daily returns in the second month preceding
    the current month. E.g. Top asset in August is the one with top mean daily
    returns in June (not July).

    Long the top asset with 100% weight unless the respective returns are -ve,
    in which case we hold cash. For the first two months we take the default
    weights given in the input data.

    Monthly re-weighting, daily rebalancing.
    NOTE: Rebalancing frequency controlled in Portfolio class. This class just
    returns weights.

    Args:
        weights_df: Dataframe of initial weights for each asset.
        prices_df: Dataframe of daily prices for each asset. We ensure only new
        day prices are used to avoid look ahead bias. Hence, the price record
        etc. below.

        NOTE: For future reference, it would be better to only pass this
        strategy the daily price in __call__ using an historical price data file
        passed to the Backtest price for generality as most strategies need
        price data.
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
            # For the first two months, return the default weights.
            if self._initial or self._second:
                self._current_weights = self.weights_df.loc[ts].to_dict()

            else:
                # Calculate the returns for each asset
                month_prices = self._prices_record[
                    ts
                    - pd.DateOffset(months=2) : ts
                    - pd.DateOffset(months=1, days=1)
                ]
                returns_df = month_prices.pct_change().dropna().mean()
                winner = returns_df.idxmax()
                # NOTE: Long-short winner minus loser could be used.
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
