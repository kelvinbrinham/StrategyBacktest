"""Momentum Strategy"""

from typing import Dict

import matplotlib.pyplot as plt  # noqa: F401
import pandas as pd

from src.strategybacktest import Backtest, BacktestAnalysis, Portfolio, Strategy


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


def run_backtest(
    initial_capital: float,
    risk_free_rate: float,
    transaction_cost: float,
    plot: bool,
    save_plots: bool = False,
) -> None:
    """
    Run the backtest.

    Args:
        initial_capital: Initial capital to invest.
        risk_free_rate: Risk free rate.
        transaction_cost: Percentage transaction cost per trade.
        plot: Plot backtest results.
        save_plots: Save backtest plots. Defaults to False.
    """
    data_filepath = ".data/weights.csv"

    # Collect data.
    # I can plot here to check for outliers. There are none.
    weights_df = pd.read_csv(data_filepath, index_col=0, parse_dates=True)
    prices_df = pd.read_csv(".data/prices.csv", index_col=0, parse_dates=True)
    # NOTE: Asset universe for future versions
    # asset_universe = list(prices_df.columns)

    # Initialise strategy
    strategy = DummyStrategy(weights_df=weights_df)

    # Initialise portfolio
    portfolio = Portfolio(
        initial_capital=initial_capital,
        price_data_source=prices_df,
        transaction_cost=transaction_cost,
    )
    # Initialise backtest
    backtest = Backtest(
        strategy=strategy,
        timestamps=prices_df.index.values,
        portfolio=portfolio,
        price_data_source=prices_df,
    )
    # Run backtest
    backtest.run_backtest()

    # Run analysis
    analyser = BacktestAnalysis(
        backtest=backtest, risk_free_rate=risk_free_rate
    )
    analyser.compute_stats()

    # Plot results
    if plot:
        analyser.plot(save=save_plots)
        analyser.underwater_plot(save=save_plots)
        analyser.volatility_plot(save=save_plots)

    # Save results to excel
    analyser.output_to_excel(
        filepath=f"output/summary_ic{initial_capital}_tc{transaction_cost}"
        f"_rf{risk_free_rate}.xlsx"
    )


if __name__ == "__main__":
    # Run backtest(s) and produce time-series and summary results as excel
    # files.
    initial_capital = 100000

    run_backtest(
        initial_capital=initial_capital,
        risk_free_rate=0,
        transaction_cost=0.003,
        plot=True,
        save_plots=True,
    )
