"""Scrap"""


positions = {"A": 100, "B": 200, "C": 3000, "D": 90}

trades = {"A": 5, "B": 200, "C": -1000, "D": -100}

dict_ = {
    ticker: position + trades[ticker] for ticker, position in positions.items()
}

print(dict_)
