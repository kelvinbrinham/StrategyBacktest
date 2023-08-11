"""Test Portfolio class."""

import pandas as pd
import pytest

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


@pytest.mark.parametrize(
    "initial_capital,expected_positions,expected_cash",
    [
        (0, {"asset1": 0, "asset2": 0, "asset3": 0}, 0),
        (0.5, {"asset1": 0, "asset2": 0, "asset3": 0}, 0.5),
        (100, {"asset1": 50, "asset2": 7, "asset3": 2}, 8),
    ],
)
def test_rebalance(
    initial_capital: float,
    expected_positions: dict,
    expected_cash: float,
    example_prices: pd.DataFrame,
    example_weights: dict,
):
    """Test Portfolio rebalance."""
    portfolio = Portfolio(
        initial_capital=initial_capital,
        price_data_source=example_prices,
        transaction_cost=0,
    )

    portfolio.rebalance(weights=example_weights, ts=pd.Timestamp("2020-01-01"))

    assert portfolio.positions == expected_positions
    assert portfolio.get_cash == expected_cash
    assert portfolio.get_NAV == initial_capital
