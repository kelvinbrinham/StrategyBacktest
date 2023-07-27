"""Backtest Class"""

import matplotlib.pyplot as plt
from portfolio import Portfolio
from strategy import Strategy


class Backtest:
    """
    Backtest class which keeps track of transactions and portfolio value.

    Args:
        strategy: strategy class
        timestamps: list of timestamps during backtest period.
    """

    def __init__(
        self, strategy: Strategy, timestamps: list, portfolio: Portfolio
    ) -> None:
        self.strategy = strategy
        self.timestamps = timestamps
        self.portfolio = portfolio
        self._NAV_record = dict()

    def run_backtest(self) -> None:
        """Run the backtest."""
        for ts in self.timestamps:
            # Get target weights
            target_weights = self.strategy(ts)

            self.portfolio.rebalance(weights=target_weights, ts=ts)

            self._NAV_record[ts] = self.portfolio.NAV

    @property
    def NAV_record(self) -> dict:
        """Return the NAV record for backtesting"""
        return self._NAV_record

    @property
    def plot(self) -> None:
        """Plot the NAV record."""
        plt.figure()
        plt.plot(self._NAV_record.keys(), self._NAV_record.values())
        plt.show()
