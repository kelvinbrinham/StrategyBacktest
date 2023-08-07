# StrategyBacktest

This is a basic strategy backtesting tool. The strategy included is a dummy strategy that takes time-series portfolio weights data and tests this strategy over historical stock data.

The backtest includes flat-rate transaction costs and includes a variable risk free rate. The risk-free rate is not yet involved in shorting but only in the calculation of Sharpe ratio!

I note a few points:

- Only whole shares are used (but this can be easily changed in the Portfolio class). Spare capital is held as cash.
- Weights change each month in the example data, but the portfolio is rebalanced daily (due to changed in share price). This can be changed in the Portfolio class. (E.g. if transaction costs are sufficiently high, one may want to rebalance less frequently).

## Installation

To install this package, clone the repository and set up a virtual poetry environment according to the `pyproject.toml` file. Then, run `poetry install` to install the dependencies.

## Usage

To run the backtest, run `poetry run python strategybacktest/main.py` from the root directory of the repository. (Alternatively run `main.py` using your IDE, but be careful of filepaths). Parameters such as risk-free rate can be changed in the `main.py` file. Feel free to look through the docstrings in the other files to see what other parameters can be changed.

The LaTeX_tables.py script can be used to generate LaTeX tables of the results from the output Excel files. The tables are saved in the `tables` directory. This is included in a separate script because one may wish to run multiple backtests and include the results in a single table produced by the LaTeX_tables.py script.

Example data is included in .data. An example output is included in Examples for the default data, 0 risk-free rate and 0.3% transaction costs.

---

### Note to self (future; in rough order of priority)

- Make into a package using poetry such that external strategies can use to backtest.
- Add risk-free rate borrowing cost to shorts.
- Add asset universe (because at the moment it is as if it is fixed).
- No execution currently. (order numbers etc.)
