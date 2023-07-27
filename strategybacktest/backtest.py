"""Backtest Class"""

from strategy import Strategy


class Backtest:
    """
    Backtest class which keeps track of transactions and portfolio value.

    Args:
        strategy: strategy class
        timestamps: list of timestamps during backtest period.
    """

    def __init__(self, strategy: Strategy, timestamps: list) -> None:
        self.strategy = strategy
        self.timestamps = timestamps
        self._NAV_record = dict()

    def run_backtest(self, initial_capital: float) -> None:
        """
        Run the backtest.

        Args:
            initial_capital: Initial capital to invest.
        """
        for ts in self.timestamps:
            # Get target weights
            target_weights = self.strategy(ts)

            # Rebalance portfolio
            self.rebalance(target_weights)
