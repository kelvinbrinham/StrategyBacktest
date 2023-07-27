"""Portfolio class for backtesting."""


from typing import Dict, List

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
        initial_weights: Dict[str, float],
        price_data_source: pd.DataFrame,
        asset_universe: List[str],
        transaction_cost: float = 0,
    ) -> None:
        self.price_data_source = price_data_source
        self.asset_universe = asset_universe
        self.transaction_cost = transaction_cost
        self.positions = {ticker: 0 for ticker in self.asset_universe}
        # self.positions = initial_weights
        # NAV includes cash
        self._NAV = initial_capital
        self._cash = initial_capital
        self._target_positions = {}
        self._prices = {}
        self._rebalance_record = {}
        self._current_weights = {}
        self._initial = True

    def rebalance(self, weights: Dict[str, float], ts: pd.Timestamp) -> None:
        """
        Rebalance portfolio according to target weights.

        Args:
            weights: Dictionary of target weights.
            ts: Timestamp for rebalance.
        """
        # Get new prices
        self._prices = self.price_data_source.loc[ts].to_dict()

        # Update NAV
        self._NAV = self._cash + self._get_net_asset_value(prices=self._prices)
        self._rebalance_record[ts] = self._NAV

        # if self._current_weights != weights:
        if True:
            # Rebalance portfolio
            # Size positions
            trades = self._position_sizer(
                target_weights=weights, prices=self._prices
            )

            # Update positions
            self.positions = {
                ticker: position + trades[ticker]
                for ticker, position in self.positions.items()
            }

        self._current_weights = weights

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
            current_position_value = self.positions[ticker] * prices[ticker]

            pre_cost_trade_value = (
                target_position_value - current_position_value
            )

            # Comission NOTE: Must check if this costs money.
            cost_trade_value = pre_cost_trade_value * (
                1 - self.transaction_cost
            )

            if self._initial:
                cost_trade_value = target_position_value

            trade_quantity = int(cost_trade_value / prices[ticker])

            if trade_quantity > 0:
                leftover_capital += (
                    cost_trade_value - trade_quantity * prices[ticker]
                )
            else:
                leftover_capital -= (
                    cost_trade_value - trade_quantity * prices[ticker]
                )

            trade_dict[ticker] = trade_quantity

        self._cash = leftover_capital
        self._initial = False
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
        for ticker, position in self.positions.items():
            net_asset_value += position * prices[ticker]

        return net_asset_value
