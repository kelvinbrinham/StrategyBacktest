"""
Main Script

I include generous comments to explain my thoughts.
"""
import sys  # noqa: F401

import matplotlib.pyplot as plt  # noqa: F401
from backtest import Backtest, BacktestAnalysis
from functions import data_collector
from portfolio import Portfolio
from strategy import DummyStrategy


def run_backtest() -> None:
    """Run the backtest."""
    data_filepath = ".data/Task.xlsx"

    # Collect data.
    # I can plot here to check for outliers. There are none.
    prices_df, weights_df = data_collector(data_filepath, plot=False)

    asset_universe = list(prices_df.columns)

    initial_capital = 100000
    risk_free_rate = 0.0
    transaction_cost = 0.0

    # Initialise strategy
    strategy = DummyStrategy(weights_df=weights_df)
    # Initialise portfolio
    portfolio = Portfolio(
        initial_capital=initial_capital,
        price_data_source=prices_df,
        asset_universe=asset_universe,
        transaction_cost=transaction_cost,
    )
    # Initialise backtest
    backtest = Backtest(
        strategy=strategy,
        timestamps=prices_df.index.values,
        portfolio=portfolio,
    )
    # Run backtest
    backtest.run_backtest()

    # Run analysis
    analyser = BacktestAnalysis(
        backtest=backtest, risk_free_rate=risk_free_rate
    )
    analyser.compute_stats()

    # Plot results
    # analyser.plot
    # analyser.underwater_plot

    # Save results to excel
    analyser.output_to_excel(filepath="output/summary.xlsx")


if __name__ == "__main__":
    run_backtest()
