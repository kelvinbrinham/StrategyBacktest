"""Test Portfolio class."""

import pandas as pd

from strategybacktest.portfolio import Portfolio


def test_init(example_prices: pd.DataFrame):
    """Test Portfolio initialization."""
    portfolio = Portfolio(
        initial_capital=100,
        price_data_source=example_prices,
        transaction_cost=0,
    )

    assert portfolio.initial_capital == 100
    assert portfolio.price_data_source.equals(example_prices)
    assert portfolio.transaction_cost == 0
    assert portfolio.positions == {}


def test_rebalance(example_prices: pd.DataFrame, example_weights: pd.DataFrame):
    """Test Portfolio rebalance."""
    portfolio = Portfolio(
        initial_capital=100,
        price_data_source=example_prices,
        transaction_cost=0,
    )

    portfolio.rebalance(weights=example_weights, ts=pd.Timestamp("2020-01-01"))

    assert portfolio.positions == {"asset1": 50, "asset2": 7, "asset3": 2}
    assert portfolio.get_cash == 8
    assert portfolio.get_NAV == 100
