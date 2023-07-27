"""Scrap"""

import numpy as np  # noqa F401
import pandas as pd  # noqa F401
from functions import data_collector

data_filepath = ".data/Task.xlsx"
prices_df, weights_df = data_collector(data_filepath, plot=False)


print(prices_df)
weights_df.to_csv("prices.csv")
# new_df = prices_df.mul(weights_df, fill_value=np.nan).dropna()
# sum_df = pd.DataFrame(new_df.sum(axis=1), columns=["Sum"])

# print(sum_df)
