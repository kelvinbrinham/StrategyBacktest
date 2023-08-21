"""Miscellaneous functions for StrategyBacktest."""

from typing import List, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd


def data_collector(
    data_filepath: str, plot: bool = False
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Collects input data from excel file, checks data is valid and returns a
    dataframe.

    Args:
        data_filepath: Filepath to excel file.
        plot: Boolean to plot price data. Defaults to False.

    Returns:
        Tuple of prices dataframe and weights dataframe.
    """
    prices_df = pd.read_excel(data_filepath, sheet_name="Data", index_col=0)
    prices_df.index = pd.to_datetime(prices_df.index, format="%Y-%d-%m")

    weights_df = pd.read_excel(data_filepath, sheet_name="Weights", index_col=0)
    weights_df.index = pd.to_datetime(weights_df.index, format="%Y-%d-%m")

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


# NOTE: I intend to make a dedicated package to do this task at some point as I
# often find myself doing it.
def excel_summary_2_latex(filepath: Union[str, List[str]]) -> None:
    """
    Convert backtest summary data from excel to LaTeX table for inclusion in
    documents.

    Args:
        filepath: Filepath to excel file(s).
    """
    if isinstance(filepath, str):
        filepath = [filepath]

    pct_columns = [
        "Transaction Cost",
        "Risk Free Rate",
        "Total Return",
        "Return (Ann.)",
        "Volatility (Ann.)",
        "Max Drawdown",
    ]

    summary_df_list = []
    for filepath_ in filepath:
        summary_df = pd.read_excel(filepath_, sheet_name="Summary")

        # Flake8 complains about the % symbol in the lambda function but it is
        # needed for writing percentages to latex table.
        summary_df[pct_columns] = summary_df[pct_columns].applymap(
            lambda x: "{:.2f}".format(100 * x) + "\%"  # noqa: W605
        )
        summary_df[["Sharpe Ratio", "Sharpe Ratio (Ann.)"]] = summary_df[
            ["Sharpe Ratio", "Sharpe Ratio (Ann.)"]
        ].applymap(lambda x: "{:.2f}".format(x))

        summary_df_format = summary_df.T
        summary_df_list.append(summary_df_format)

    summary_df_format = pd.concat(summary_df_list, axis=1)

    caption = "Portfolio performance summary; daily rebalancing."

    output_filename = filepath_[15:]
    with open(f"output_tables/table_{output_filename}.tex", "w") as f:
        f.write("\\begin{table}[p]\n")
        f.write("\\centering\n")
        f.write("\\caption{" + f"{caption}" + "}\n")

        latex_table = summary_df_format.to_latex(
            escape=False, header=False, index=True, column_format="rrrrrrr"
        )

        # Split the LaTeX table into lines
        lines = latex_table.split("\n")

        # Insert \hrule after the second row
        lines.insert(5, r"\hline")

        # Write the modified LaTeX table back to the file
        f.write("\n".join(lines))

        f.write("\\end{table}\n")
