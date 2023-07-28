# StrategyBacktest

This is a basic strategy backtesting tool. The strategy included is a dummy strategy that takes time-series portfolio weights data and tests this strategy over historical stock data.

The backtest includes flat-rate transaction costs and includes a variable risk free rate. The risk-free rate is not yet involved in shorting but only in the calculation of Sharpe ratio!

## Installation

To install this package, clone the repository and set up a virtual poetry environment according to the `pyproject.toml` file. Then, run `poetry install` to install the dependencies.

---
