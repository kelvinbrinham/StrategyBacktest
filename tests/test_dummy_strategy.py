"""Test DummyStrategy class."""

import pandas as pd

from strategybacktest.strategy import DummyStrategy


def test_init(example_weights_df: pd.DataFrame):
    """Test DummyStrategy initialization."""
    strategy = DummyStrategy(weights_df=example_weights_df)

    assert strategy.weights_df.equals(example_weights_df)
    assert strategy._current_weights == {}


def test_call(
    example_weights_df: pd.DataFrame,
    example_ts: pd.Timestamp,
    example_weights: dict,
):
    """Test new day weights generation."""
    strategy = DummyStrategy(weights_df=example_weights_df)
    strategy(ts=example_ts)

    assert strategy._current_weights == example_weights
