# StrategyBacktest

This is a basic strategy backtesting package. An example dummy strategy is included in the `example_strategies/dummy_strategy.py` script which shows how to use the package.

The backtest includes flat-rate transaction costs and includes a variable risk free rate. The risk-free rate is not yet involved in shorting but only in the calculation of Sharpe ratio!

I note a few points:

- Only whole shares are used (but this can be easily changed in the Portfolio class). Spare capital is held as cash.
- Weights change each month in the example data, but the portfolio is rebalanced daily (due to changed in share price). This can be changed in the Portfolio class. (E.g. if transaction costs are sufficiently high, one may want to rebalance less frequently).

## Installation

To install this package, add the repo and relevant release branch to your `pyproject.toml` file and run `poetry install`. (I recommend using poetry to manage your virtual environment).

## Usage

To backtest your strategy, install the package and run the backtest in the same way as in `example_strategies/dummy_strategy.py`. Parameters such as risk-free rate can be changed. Feel free to look through the docstrings in the package files for more information. You should have folders named `.data` and `output` in your strategy repo.

The LaTeX_tables.py script can be used to generate LaTeX tables of the results from the output Excel files. The tables are saved in the `tables` directory. This is included in a separate script because one may wish to run multiple backtests and include the results in a single table produced by the LaTeX_tables.py script.

---

### Note to self (future; in rough order of priority)

- Add validation for parameters
- Add risk-free rate borrowing cost to shorts.
- Add asset universe (because at the moment it is as if it is fixed).
- No execution currently. (order numbers etc.)
