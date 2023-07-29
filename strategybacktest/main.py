"""
Main Script

I include generous comments to explain my thoughts.
"""

import matplotlib.pyplot as plt  # noqa: F401
from backtest import Backtest, BacktestAnalysis
from functions import data_collector
from portfolio import Portfolio
from strategy import DummyStrategy


def run_backtest(
    initial_capital: float, risk_free_rate: float, transaction_cost: float
) -> None:
    """
    Run the backtest.

    Args:
        initial_capital: Initial capital to invest.
        risk_free_rate: Risk free rate.
        transaction_cost: Percentage transaction cost per trade.
    """
    data_filepath = ".data/Task.xlsx"

    # Collect data.
    # I can plot here to check for outliers. There are none.
    prices_df, weights_df = data_collector(data_filepath, plot=False)

    asset_universe = list(prices_df.columns)

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
    # save_plots = True
    # analyser.plot(save=save_plots)
    # analyser.underwater_plot(save=save_plots)
    # analyser.volatility_plot(save=save_plots)

    # Save results to excel
    analyser.output_to_excel(
        filepath=f"output/summary_ic{initial_capital}_tc{transaction_cost}"
        f" _rf{risk_free_rate}.xlsx"
    )


if __name__ == "__main__":
    # Run backtest and produce time-series and summary results as excel files.
    initial_capital = 1000000
    risk_free_rate = [0, 0.015]
    transaction_cost = [0.003, 0]
    run_backtest(
        initial_capital=initial_capital,
        risk_free_rate=0,
        transaction_cost=0.003,
    )

    for risk_free_rate_ in risk_free_rate:
        for transaction_cost_ in transaction_cost:
            run_backtest(
                initial_capital=initial_capital,
                risk_free_rate=risk_free_rate_,
                transaction_cost=transaction_cost_,
            )
