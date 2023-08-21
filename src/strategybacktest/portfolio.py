"""Portfolio class for backtesting."""


from typing import Dict

import pandas as pd


class Portfolio:
    """
    Class to keep track of portfolio value, positions and execute trades
    (changes in position as we of course do not have access to the market here).

    NOTE: For future reference, asset universe would be included in the strategy
    class such that the portfolio class can be used for multiple strategies. If
    an asset was delisted, the strategy would return a zero weight for this
    asset so it could be removed from the portfolio. As of now we have a
    constant universe.

    Args:
        initial_capital: Initial capital to invest.
        price_data_source: Pricing data source e.g. API. In this case, it is
        just a predetermined dataframe.
        transaction_cost: Percentage transaction
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
        # NOTE: If an asset is absent in self.positions => asset position is 0.
        # (We therefore do not have 0's in self.positions)
        self.positions = dict()
        self.initial_capital = initial_capital
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
        # Get new ts prices
        self._prices = self.price_data_source.loc[ts].to_dict()

        # Update NAV from positions and new prices.
        # NOTE: NAV is calculated before rebalancing, it is the same after
        # rebalancing on the same day and so we just calculate it here. This is
        # by construction because the rebalancing occurs with a budget of NAV
        # calculated here, so it will be the same after rebalancing even if
        # positions change.
        self._NAV = self._cash + self._get_net_asset_value(prices=self._prices)

        # Record NAV for current day (BEFORE rebalance)
        self._rebalance_record[ts] = self._NAV

        # NOTE: Frequency of rebalancing is determined here.
        # Monthly rebalancing (Rebalance according to weights_df in input data).
        # if self._current_weights != weights:
        # Daily rebalancing. (Rebalance every day of the backtest).
        if True:
            # Size trades from weights.
            trades = self._position_sizer(
                target_weights=weights, prices=self._prices
            )

            # Update positions
            self.positions = {
                k: self.positions.get(k, 0) + trades.get(k, 0)
                for k in set(self.positions) | set(trades)
            }

            # Update cash
            self._cash = self._NAV - self._get_net_asset_value(
                prices=self._prices
            )

        self._current_weights = weights

    @property
    def get_NAV(self) -> float:
        """Return the NAV for backtest statistics."""
        return self._NAV

    @property
    def get_initial_capital(self) -> float:
        """Return the Initial Capital for backtesting."""
        return self.initial_capital

    @property
    def get_cash(self) -> float:
        """Return the Cash for backtesting."""
        return self._cash

    def _position_sizer(
        self, target_weights: Dict[str, float], prices: Dict[str, float]
    ) -> Dict[str, int]:
        """
        Calculate number of shares to buy for the target weights.

        Args:
            target_weights: Target weights for each asset.
            prices: Current prices for each asset.

        Returns:
            Dictionary of trades (number of positions to purchase) for each
            asset.
        """
        trade_dict = dict()
        for ticker, target_weight in target_weights.items():
            # NOTE: We assume buy and sell price are the same given the data in
            # this simpler prescription.
            target_position_value = self._NAV * target_weight

            if ticker in self.positions:
                current_position_value = self.positions[ticker] * prices[ticker]
            else:
                current_position_value = 0

            pre_cost_trade_value = (
                target_position_value - current_position_value
            )

            # Comission NOTE: Must check if this costs money.
            cost_trade_value = pre_cost_trade_value * (
                1 - self.transaction_cost
            )

            # NOTE: We assume no transaction cost for initial positions. I.e.
            # assume initial positions are already held.
            if self._initial:
                cost_trade_value = target_position_value

            # Whole shares
            trade_quantity = int(cost_trade_value / prices[ticker])
            # Fractional shares
            # trade_quantity = cost_trade_value / prices[ticker]

            trade_dict[ticker] = trade_quantity

        self._initial = False
        return trade_dict

    def _get_net_asset_value(self, prices: Dict[str, float]) -> float:
        """
        Get the current asset value (NAV - cash).

        Args:
            prices: Current asset prices.

        Returns:
            Current market value of all positions held.
        """
        total_asset_value = 0
        for ticker, position in self.positions.items():
            total_asset_value += position * prices[ticker]

        return total_asset_value
