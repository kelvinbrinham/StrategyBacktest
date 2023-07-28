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

data_filepath = ".data/Task.xlsx"

# Collect data.
# I can plot here to check for outliers. There are none.
prices_df, weights_df = data_collector(data_filepath, plot=False)
# plt.show()

# Initialise the backtest
asset_universe = list(prices_df.columns)

initial_capital = 1000000
strategy = DummyStrategy(weights_df=weights_df)

portfolio = Portfolio(
    initial_capital=initial_capital,
    price_data_source=prices_df,
    asset_universe=asset_universe,
    transaction_cost=0.00,
)

backtest = Backtest(
    strategy=strategy, timestamps=prices_df.index.values, portfolio=portfolio
)

backtest.run_backtest()


# Analysis
analyser = BacktestAnalysis(backtest=backtest, risk_free_rate=0.0)
analyser.compute_stats()

stats = analyser.stats
summary_stats = analyser.summary_stats

analyser.plot
analyser.underwater_plot


analyser.output_to_excel(filepath="output/summary.xlsx")
