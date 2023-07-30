"""Main Script for running the backtest."""

import matplotlib.pyplot as plt  # noqa: F401
from backtest import Backtest, BacktestAnalysis
from functions import data_collector
from portfolio import Portfolio
from strategy import DummyStrategy, Momentum  # noqa: F401


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

    # NOTE: Asset universe for future versions
    # asset_universe = list(prices_df.columns)

    # Initialise strategy
    strategy = DummyStrategy(weights_df=weights_df)
    # strategy = Momentum(weights_df=weights_df, prices_df=prices_df)

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
    save_plots = False
    analyser.plot(save=save_plots)
    analyser.underwater_plot(save=save_plots)
    analyser.volatility_plot(save=save_plots)

    # Save results to excel
    analyser.output_to_excel(
        filepath=f"output/summary_ic{initial_capital}_tc{transaction_cost}"
        f" _rf{risk_free_rate}.xlsx"
    )


if __name__ == "__main__":
    # Run backtest(s) and produce time-series and summary results as excel
    # files.
    initial_capital = 1000000

    run_backtest(
        initial_capital=initial_capital,
        risk_free_rate=0,
        transaction_cost=0,
    )

    # Run multiple backtests
    # risk_free_rate = [0, 0.015]
    # transaction_cost = [0.003, 0]
    # for risk_free_rate_ in risk_free_rate:
    #     for transaction_cost_ in transaction_cost:
    #         run_backtest(
    #             initial_capital=initial_capital,
    #             risk_free_rate=risk_free_rate_,
    #             transaction_cost=transaction_cost_,
    #         )
