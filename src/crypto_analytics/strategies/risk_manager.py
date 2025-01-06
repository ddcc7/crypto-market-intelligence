"""Risk management module for adaptive position sizing and dynamic risk levels."""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class RiskMetrics:
    """Container for risk metrics."""

    kelly_fraction: float
    position_size: float
    stop_loss: float
    take_profit: float
    risk_ratio: float
    volatility_factor: float


class AdaptiveRiskManager:
    """Adaptive position sizing and risk management system."""

    def __init__(
        self,
        base_position_size: float = 1.0,
        max_position_size: float = 2.0,
        min_position_size: float = 0.1,
        base_stop_loss: float = 0.02,
        base_take_profit: float = 0.04,
        lookback_period: int = 20,
        volatility_scaling: bool = True,
        kelly_fraction: float = 0.5,  # Half-Kelly for more conservative sizing
    ):
        """Initialize risk manager.

        Args:
            base_position_size: Base position size as fraction of capital
            max_position_size: Maximum allowed position size
            min_position_size: Minimum allowed position size
            base_stop_loss: Base stop-loss percentage
            base_take_profit: Base take-profit percentage
            lookback_period: Period for calculating metrics
            volatility_scaling: Whether to scale by volatility
            kelly_fraction: Fraction of Kelly criterion to use
        """
        self.base_position_size = base_position_size
        self.max_position_size = max_position_size
        self.min_position_size = min_position_size
        self.base_stop_loss = base_stop_loss
        self.base_take_profit = base_take_profit
        self.lookback_period = lookback_period
        self.volatility_scaling = volatility_scaling
        self.kelly_fraction = kelly_fraction

    def calculate_kelly_fraction(
        self, historical_returns: pd.Series, win_rate: float
    ) -> float:
        """Calculate optimal Kelly fraction.

        Args:
            historical_returns: Series of historical returns
            win_rate: Historical win rate

        Returns:
            Optimal Kelly fraction
        """
        if len(historical_returns) == 0 or win_rate == 0:
            return 0.0

        # Calculate average win and loss sizes
        wins = historical_returns[historical_returns > 0]
        losses = historical_returns[historical_returns < 0]

        avg_win = wins.mean() if len(wins) > 0 else 0
        avg_loss = abs(losses.mean()) if len(losses) > 0 else float("inf")

        # Kelly Criterion formula: f = (p/q) * (b/a) - (q/p)
        # where p = win probability, q = loss probability
        # b = average win, a = average loss
        if avg_loss == 0 or np.isinf(avg_loss):
            return 0.0

        q = 1 - win_rate
        kelly = (win_rate / q) * (avg_win / avg_loss) - (q / win_rate)

        # Apply fraction and constraints
        kelly = max(0.0, min(1.0, kelly * self.kelly_fraction))
        return kelly

    def calculate_volatility_factor(self, returns: pd.Series) -> float:
        """Calculate volatility scaling factor.

        Args:
            returns: Series of returns

        Returns:
            Volatility scaling factor
        """
        if not self.volatility_scaling or len(returns) < self.lookback_period:
            return 1.0

        # Calculate rolling volatility
        vol = returns.rolling(self.lookback_period).std()
        current_vol = vol.iloc[-1]
        avg_vol = vol.mean()

        if avg_vol == 0:
            return 1.0

        # Scale factor inversely with volatility
        vol_factor = avg_vol / current_vol
        return np.clip(vol_factor, 0.5, 2.0)

    def calculate_dynamic_levels(
        self, returns: pd.Series, volatility_factor: float
    ) -> Tuple[float, float]:
        """Calculate dynamic stop-loss and take-profit levels.

        Args:
            returns: Series of returns
            volatility_factor: Volatility scaling factor

        Returns:
            Tuple of (stop_loss, take_profit) levels
        """
        if len(returns) < self.lookback_period:
            return self.base_stop_loss, self.base_take_profit

        # Calculate ATR-based levels
        high_low_range = (
            returns.rolling(self.lookback_period).max()
            - returns.rolling(self.lookback_period).min()
        )
        atr = high_low_range.mean()

        # Scale base levels with ATR and volatility
        stop_loss = self.base_stop_loss * (1 + atr) * volatility_factor
        take_profit = self.base_take_profit * (1 + atr) * volatility_factor

        # Ensure reasonable limits
        stop_loss = np.clip(
            stop_loss, self.base_stop_loss * 0.5, self.base_stop_loss * 2.0
        )
        take_profit = np.clip(
            take_profit, self.base_take_profit * 0.5, self.base_take_profit * 2.0
        )

        return float(stop_loss), float(take_profit)

    def calculate_position_size(
        self, kelly_fraction: float, volatility_factor: float, risk_ratio: float
    ) -> float:
        """Calculate optimal position size.

        Args:
            kelly_fraction: Kelly criterion fraction
            volatility_factor: Volatility scaling factor
            risk_ratio: Risk-reward ratio

        Returns:
            Optimal position size
        """
        # Base size adjusted by Kelly and volatility
        position_size = self.base_position_size * kelly_fraction * volatility_factor

        # Scale by risk-reward ratio
        if risk_ratio > 0:
            position_size *= np.sqrt(risk_ratio)

        # Apply limits
        return np.clip(position_size, self.min_position_size, self.max_position_size)

    def get_risk_metrics(
        self, data: pd.DataFrame, signals: pd.DataFrame
    ) -> RiskMetrics:
        """Calculate all risk metrics for position sizing.

        Args:
            data: DataFrame with OHLCV data
            signals: DataFrame with trading signals

        Returns:
            RiskMetrics object with all calculated metrics
        """
        # Calculate historical returns and win rate
        returns = signals["strategy_returns"].dropna()
        win_rate = (returns > 0).mean() if len(returns) > 0 else 0

        # Calculate Kelly fraction
        kelly = self.calculate_kelly_fraction(returns, win_rate)

        # Calculate volatility factor
        vol_factor = self.calculate_volatility_factor(returns)

        # Calculate dynamic stop-loss and take-profit
        stop_loss, take_profit = self.calculate_dynamic_levels(returns, vol_factor)

        # Calculate risk-reward ratio
        risk_ratio = take_profit / stop_loss if stop_loss > 0 else 0

        # Calculate final position size
        position_size = self.calculate_position_size(kelly, vol_factor, risk_ratio)

        return RiskMetrics(
            kelly_fraction=kelly,
            position_size=position_size,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_ratio=risk_ratio,
            volatility_factor=vol_factor,
        )

    def apply_risk_management(
        self, signals: pd.DataFrame, metrics: Optional[RiskMetrics] = None
    ) -> pd.DataFrame:
        """Apply risk management rules to trading signals.

        Args:
            signals: DataFrame with trading signals
            metrics: Optional pre-calculated risk metrics

        Returns:
            DataFrame with risk-adjusted signals
        """
        if metrics is None:
            metrics = self.get_risk_metrics(signals, signals)

        # Apply position sizing
        signals["position"] = signals["position"] * metrics.position_size

        # Apply stop-loss and take-profit
        for i in range(1, len(signals)):
            if signals.iloc[i - 1]["position"] != 0:
                returns = (
                    signals.iloc[i]["close"] - signals.iloc[i - 1]["close"]
                ) / signals.iloc[i - 1]["close"]

                if returns * signals.iloc[i - 1]["position"] <= -metrics.stop_loss:
                    # Stop loss hit
                    signals.iloc[i, signals.columns.get_loc("signal")] = -signals.iloc[
                        i - 1
                    ]["position"]
                    signals.iloc[i, signals.columns.get_loc("position")] = 0
                    signals.iloc[i, signals.columns.get_loc("strategy_returns")] = (
                        -metrics.stop_loss
                    )
                elif returns * signals.iloc[i - 1]["position"] >= metrics.take_profit:
                    # Take profit hit
                    signals.iloc[i, signals.columns.get_loc("signal")] = -signals.iloc[
                        i - 1
                    ]["position"]
                    signals.iloc[i, signals.columns.get_loc("position")] = 0
                    signals.iloc[i, signals.columns.get_loc("strategy_returns")] = (
                        metrics.take_profit
                    )

        return signals
