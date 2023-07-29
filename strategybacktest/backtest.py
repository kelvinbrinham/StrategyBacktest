"""Backtest Class"""

from typing import Tuple

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
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


class BacktestAnalysis:
    """
    Compute backtest statistics.

    Args:
        backtest: Backtest class.
        risk_free_rate: (annual) Risk free rate. Defaults to 0.
    """

    def __init__(self, backtest: Backtest, risk_free_rate: float = 0) -> None:
        self.backtest = backtest
        self.risk_free_rate = risk_free_rate
        self._NAV_record = backtest.NAV_record
        # Create out dataframe
        self._stats = pd.DataFrame(self._NAV_record, index=["NAV"]).T
        self._summary_stats = pd.DataFrame([np.nan])
        self._daily_drawdown = pd.Series()
        self._max_daily_drawdown = pd.Series()
        self._drawdown_duration_max = int()
        self._compute_stats = False

    def compute_stats(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Compute backtest statistics."""
        self._compute_stats = True
        self._compute_returns()
        self._compute_total_volatility()
        self._compute_sharpe_ratio()
        self._compute_max_drawdown()
        self._compute_longest_drawdown()
        self._construct_summary_stats()
        # Clean up
        self._stats = self._stats.drop(
            columns=["Volatility", "Max Drawdown", "Sharpe Ratio"]
        )
        self._summary_stats = self._summary_stats.drop(columns=[0])

    def output_to_excel(self, filepath: str) -> None:
        """
        Output stats to excel.

        Args:
            filepath: Filepath to output excel file.
        """
        if not self._compute_stats:
            raise ValueError("Please run compute_stats() first.")

        writer = pd.ExcelWriter(filepath, engine="xlsxwriter")

        self._summary_stats.to_excel(writer, sheet_name="Summary", index=False)
        self._stats.to_excel(writer, sheet_name="Time Series", index=True)
        percent_format = writer.book.add_format({"num_format": "0.00%"})
        # Now apply the number format to the column with index 2.
        writer.sheets["Time Series"].set_column(2, 3, 15, percent_format)
        writer.sheets["Summary"].set_column(0, 1, 20, percent_format)
        writer.sheets["Summary"].set_column(2, 3, 20, percent_format)
        writer.sheets["Summary"].set_column(4, 5, 20)
        writer.sheets["Summary"].set_column(6, 7, 20, percent_format)
        writer.sheets["Summary"].set_column(8, 9, 30)

        writer.close()

    @property
    def stats(self) -> pd.DataFrame:
        """Return the stats dataframe."""
        if not self._compute_stats:
            raise ValueError("Please run compute_stats() first.")
        return self._stats

    @property
    def summary_stats(self) -> pd.DataFrame:
        """Return the stats dataframe."""
        if not self._compute_stats:
            raise ValueError("Please run compute_stats() first.")
        return self._summary_stats

    @property
    def plot(self) -> None:
        """Plot the NAV record."""
        plt.figure()
        normalised_NAV_record = [
            NAV / self.backtest.portfolio.get_initial_capital
            for NAV in self._NAV_record.values()
        ]
        plt.plot(self._NAV_record.keys(), normalised_NAV_record)
        plt.title(
            "NAV - Daily Rebalancing -"
            f" {self.backtest.portfolio.transaction_cost * 100}%"
            " Transaction Cost"
        )
        plt.ylabel("NAV / Initial Capital")
        plt.xlabel("Date")
        plt.show()

    @property
    def underwater_plot(self) -> None:
        """Plot the drawdowns."""
        if not self._compute_stats:
            raise ValueError("Please run compute_stats() first.")
        fig, ax = plt.subplots()
        ax.plot(
            self._daily_drawdown.index,
            self._daily_drawdown * 100,
            label="Daily Drawdown",
        )
        ax.plot(
            self._max_daily_drawdown.index,
            self._max_daily_drawdown * 100,
            label="Max Daily Drawdown",
        )
        ax.set_title("Underwater Chart")
        ax.set_ylabel("Drawdown")
        ax.set_xlabel("Date")
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
        ax.legend(loc="lower left")
        plt.show()

    @property
    def volatility_plot(self) -> None:
        """Plot the volatility."""
        plt.figure()
        rolling_volatility = self._rolling_volatility()
        if not self._compute_stats:
            raise ValueError("Please run compute_stats() first.")
        fig, ax = plt.subplots()
        ax.plot(
            rolling_volatility.index,
            rolling_volatility * 100,
            label="Daily Drawdown",
        )
        ax.set_title("Rolling 21 day Volatility")
        ax.set_ylabel("Rolling 21 day Volatility (Ann.)")
        ax.set_xlabel("Date")
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1))
        plt.show()

    def _construct_summary_stats(self) -> None:
        """Construct dataframe of summary statistics for entire backtest."""
        self._summary_stats[
            "Transaction Cost"
        ] = self.backtest.portfolio.transaction_cost
        self._summary_stats["Risk Free Rate"] = self.risk_free_rate
        self._summary_stats["Total Return"] = (
            self._stats["NAV"].iloc[-1] / self._stats["NAV"].iloc[0] - 1
        )
        self._summary_stats["Return (Ann.)"] = (
            1 + self._summary_stats["Total Return"]
        ) ** (252 / len(self._stats)) - 1
        self._summary_stats["Sharpe Ratio"] = self._stats["Sharpe Ratio"].mean()
        self._summary_stats["Sharpe Ratio (Ann.)"] = (
            np.sqrt(252 / (len(self._stats) - 1))
            * self._summary_stats["Sharpe Ratio"]
        )
        self._summary_stats["Volatility (Ann.)"] = self._stats[
            "Volatility"
        ].mean() * np.sqrt(252 / (len(self._stats) - 1))
        self._summary_stats["Max Drawdown"] = abs(
            self._stats["Max Drawdown"].min()
        )
        self._summary_stats["Max Drawdown Date"] = (
            self._stats["Max Drawdown"].idxmin().strftime("%Y-%m-%d")
        )
        self._summary_stats[
            "Longest Drawdown (Days)"
        ] = self._drawdown_duration_max

    def _compute_returns(self) -> None:
        """Compute (cumulative) returns."""
        self._stats["Returns"] = self._stats["NAV"].pct_change()
        self._stats["Cumulative Returns"] = (
            1 + self._stats["Returns"]
        ).cumprod() - 1
        self._stats = self._stats.fillna(0)

    def _compute_total_volatility(self) -> None:
        """Compute volatility."""
        # Ignore first value which is not physical
        self._stats["Volatility"] = self._stats["Returns"][1:].std() * np.sqrt(
            len(self._stats) - 1
        )

    def _rolling_volatility(self) -> pd.Series:
        """Compute rolling 21 day volatility."""
        rolling_volatility = self._stats["Returns"][1:].rolling(
            21
        ).std() * np.sqrt(252)

        return rolling_volatility

    def _compute_sharpe_ratio(self) -> None:
        """Compute the (annualised) sharpe ratio."""
        # Convert risk free rate to daily
        risk_free_rate = self.risk_free_rate / 252
        self._stats["Sharpe Ratio"] = (
            (len(self._stats) - 1)
            # Mean daily returns including risk free rate deduction
            * (self._stats["Returns"][1:] - risk_free_rate).mean()
            / self._stats["Volatility"].values[0]
        )

    def _compute_max_drawdown(self) -> None:
        """Compute the maximum drawdown."""
        rolling_max_NAV = (
            self._stats["NAV"].rolling(len(self._stats), min_periods=1).max()
        )
        self._daily_drawdown = self._stats["NAV"] / rolling_max_NAV - 1.0
        self._max_daily_drawdown = self._daily_drawdown.rolling(
            len(self._stats), min_periods=1
        ).min()
        # Max drawdown so far
        self._stats["Max Drawdown"] = self._max_daily_drawdown

    def _compute_longest_drawdown(self) -> None:
        """Compute the longest drawdown."""
        start_end_drawdowns = self._daily_drawdown.drop(
            self._daily_drawdown[self._daily_drawdown != 0].index
        )
        drawdown_durations = (
            start_end_drawdowns.index.to_series().diff().dt.days
        )
        end_date = self._daily_drawdown.index[-1]
        if end_date not in start_end_drawdowns.index:
            drawdown_durations[end_date] = (
                end_date - start_end_drawdowns.index[-1]
            ).days
        self._drawdown_duration_max = drawdown_durations.max()
