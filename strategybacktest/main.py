"""
Main Script

I include generous comments to explain my thoughts.
"""

import matplotlib.pyplot as plt  # noqa: F401
import pandas as pd
from functions import data_collector

data_filepath = ".data/Task.xlsx"

# Collect data.
# I can plot here to check for outliers. There are none.
prices_df, weights_df = data_collector(data_filepath, plot=False)
# plt.show()

ts = pd.Timestamp("2003-07-02")

print(weights_df.loc[ts].to_dict())
