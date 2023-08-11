"""Conftest for tests."""

import pandas as pd
import pytest


@pytest.fixture
def example_ts():
    """Example prices for testing."""
    return pd.date_range("2020-01-01", periods=3, freq="D")[0]


@pytest.fixture
def example_prices():
    """Example prices for testing."""
    ts = pd.date_range("2020-01-01", periods=3, freq="D")
    return pd.DataFrame(
        {
            "asset1": [1, 2, 3],
            "asset2": [4, 5, 6],
            "asset3": [7, 8, 9],
        },
        index=ts,
    )


@pytest.fixture
def example_weights():
    """Example weights dictionary for testing."""
    return {"asset1": 0.5, "asset2": 0.3, "asset3": 0.2}


@pytest.fixture
def example_weights_df():
    """Example weights dataframe for testing."""
    ts = pd.date_range("2020-01-01", periods=3, freq="D")
    return pd.DataFrame(
        {
            "asset1": 0.5,
            "asset2": 0.3,
            "asset3": 0.2,
        },
        index=ts,
    )
