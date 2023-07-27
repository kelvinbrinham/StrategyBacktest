"""
Main Script

I include generous comments to explain my thoughts.
"""

import matplotlib.pyplot as plt  # noqa: F401
import pandas as pd
from backtest import Backtest
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

initial_capital = 10000000
strategy = DummyStrategy(weights_df=weights_df)

portfolio = Portfolio(
    initial_capital=initial_capital,
    price_data_source=prices_df,
    asset_universe=asset_universe,
    transaction_cost=0.05,
)

backtest = Backtest(
    strategy=strategy, timestamps=prices_df.index, portfolio=portfolio
)

backtest.run_backtest()

# print(backtest.NAV_record)
# Plot the NAV
plt.figure()
pd.Series(backtest._NAV_record).plot()

# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
portfolio = Portfolio(
    initial_capital=initial_capital,
    price_data_source=prices_df,
    asset_universe=asset_universe,
    transaction_cost=0,
)

backtest = Backtest(
    strategy=strategy, timestamps=prices_df.index, portfolio=portfolio
)

backtest.run_backtest()

# print(backtest.NAV_record)
# Plot the NAV
pd.Series(backtest._NAV_record).plot()
plt.show()
