"""Portfolio class for backtesting."""


from typing import Dict

import pandas as pd


class Portfolio:
    """
    Class to keep track of portfolio value and transactions.

    Args:
        initial_capital: Initial capital to invest.
        price_data_source: Pricing data source e.g. API. In this case, it is
        just a predetermined dataframe. transaction_cost: Percentage transaction
        cost per trade. Defaults to 0.
    """

    def __init__(
        self,
        initial_capital: float,
        price_data_source: pd.DataFrame,
        transaction_cost: float = 0,
    ) -> None:
        self.price_data_source = price_data_source
        self.transaction_cost = transaction_cost
        # NAV includes cash
        self._NAV = initial_capital
        self._cash = initial_capital
        # {ticker: number of shares}
        self._positions = {}
        self._target_positions = {}
        self._prices = {}
        self._current_weights = {}

    def rebalance(self, weights: Dict[str, float], ts: pd.Timestamp) -> None:
        """
        Rebalance portfolio according to target weights.

        Args:
            weights: Dictionary of target weights.
            ts: Timestamp for rebalance.
        """
        # Get new prices
        self._prices = self.price_data_source.loc[ts].to_dict()

        # Rebalance portfolio
        # Size positions
        trades = self._position_sizer(
            target_weights=weights, prices=self._prices
        )

        # Update positions
        self._positions = {
            ticker: position + trades[ticker]
            for ticker, position in self._positions.items()
        }

        # Update NAV
        self._NAV = self._cash + self._get_net_asset_value(prices=self._prices)

    @property
    def NAV(self) -> float:
        """Return the NAV for backtesting"""
        return self._NAV

    def _position_sizer(
        self, target_weights: Dict[str, float], prices: Dict[str, float]
    ) -> Dict[str, int]:
        """
        Calculate number of shares to buy for the target weights.

        Args:
            target_weights: Target weights for each stock.
            prices: Current prices for each stock.

        Returns:
            Dictionary of new position sizes for each stock.
        """
        trade_dict = dict()
        leftover_capital = 0
        for ticker, target_weight in target_weights.items():
            # Calculate number of shares
            # NOTE: We assume buy and sell price are the same given the data.
            target_position_value = self._NAV * target_weight
            current_position_value = self._NAV * self._current_weights.get(
                ticker, 0
            )

            pre_cost_trade_value = (
                target_position_value - current_position_value
            )

            # Comission
            cost_trade_value = pre_cost_trade_value * (
                1 - self.transaction_cost
            )

            trade_quantity = int(cost_trade_value / prices[ticker])
            leftover_capital += (
                cost_trade_value - trade_quantity * prices[ticker]
            )

            trade_dict[ticker] = trade_quantity

        self._cash = leftover_capital
        return trade_dict

    def _get_net_asset_value(self, prices: Dict[str, float]) -> float:
        """
        Get the current NAV

        Args:
            prices: _description_

        Returns:
            Current market value of all assets.
        """
        net_asset_value = 0
        for ticker, position in self._positions.items():
            net_asset_value += position * prices[ticker]

        return net_asset_value
