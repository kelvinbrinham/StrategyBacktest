"""Miscallaneous functions for backtesting strategies."""

from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd


def data_collector(
    data_filepath: str, plot: bool = False
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Collects data from excel file, checks data is valid and returns a
    dataframe.

    Args:
        data_filepath: filepath to excel file.
        plot: boolean to plot price data. Defaults to False.

    Returns:
        Tuple of prices dataframe and weights dataframe.
    """
    prices_df = pd.read_excel(data_filepath, sheet_name="Data", index_col=0)
    prices_df.index = pd.to_datetime(prices_df.index)

    weights_df = pd.read_excel(data_filepath, sheet_name="Weights", index_col=0)
    weights_df.index = pd.to_datetime(weights_df.index)

    # Check prices are valid
    if (prices_df <= 0).any().any():
        raise ValueError("Price data contains negative values.")

    # Check total weights are valid
    if any(weights_df.sum(axis=1)) != 1:
        raise ValueError("Total weights do not sum to 1.")

    if plot:
        plt.figure()
        for ticker in prices_df.columns:
            prices_df[ticker].plot()
            plt.title("Price Data")
            plt.legend()

    return prices_df, weights_df


# NOTE: Maybe not needed
def get_difference_between_dictionaries(
    target_positions: dict, positions: dict
) -> dict:
    """
    Gets the difference between two dictionaries.
    NOTE: Courtesy of https://stackoverflow.com/questions/4527942/comparing-two
    -dictionaries-in-python

    Args:
        target_positions: The target dictionary.
        positions: The dictionary to compare to the target dictionary.

    Returns:
        A dictionary containing the differences between the two dictionaries.
    """
    new_dict = {}
    for key, value in target_positions.items():
        if key not in positions:
            new_dict[key] = value
        elif value != positions.get(key, None):
            new_dict[key] = value - positions.get(key, 0)
        else:
            new_dict[key] = 0
    for key in positions:
        if key not in target_positions:
            new_dict[key] = positions[key]
            new_dict[key] = -new_dict[key]
    return new_dict
