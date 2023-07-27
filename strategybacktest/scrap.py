"""Scrap"""

import numpy as np
import pandas as pd
from functions import data_collector

data_filepath = ".data/Task.xlsx"
prices_df, weights_df = data_collector(data_filepath, plot=False)


new_df = prices_df.mul(weights_df, fill_value=np.nan).dropna()
sum_df = pd.DataFrame(new_df.sum(axis=1), columns=["Sum"])

print(sum_df)
