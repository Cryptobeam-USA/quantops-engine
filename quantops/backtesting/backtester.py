"""Backtesting framework for testing trading strategies."""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd
import numpy as np

from quantops.strategies.base import BaseStrategy

logger = logging.getLogger(__name__)


class Backtester:
    """
    Backtesting engine for evaluating trading strategies on historical data.
    """
    
    def __init__(
        self,
        initial_capital: float = 100000.0,
        commission: float = 0.001,
        slippage: float = 0.0005
    ):
        """
        Initialize backtester.
        
        Args:
            initial_capital: Starting capital for backtest
            commission: Trading commission (0.001 = 0.1%)
            slippage: Slippage factor (0.0005 = 0.05%)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.reset()
        
        logger.info(f"Backtester initialized with ${initial_capital} capital")
    
    def reset(self) -> None:
        """Reset backtester state."""
        self.capital = self.initial_capital
        self.positions: Dict[str, float] = {}
        self.trades: List[Dict[str, Any]] = []
        self.equity_curve: List[float] = [self.initial_capital]
        self.timestamps: List[datetime] = []
    
    async def run(
        self,
        strategy: BaseStrategy,
        historical_data: Dict[str, pd.DataFrame],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Run backtest on historical data.
        
        Args:
            strategy: Strategy to backtest
            historical_data: Dictionary of historical OHLCV dataframes by symbol
            start_date: Optional start date for backtest
            end_date: Optional end date for backtest
            
        Returns:
            Dictionary containing backtest results and metrics
        """
        self.reset()
        logger.info(f"Starting backtest for {strategy.name}")
        
        # Get the first symbol's data to iterate through time
        primary_symbol = list(historical_data.keys())[0]
        df = historical_data[primary_symbol]
        
        # Filter by date range if specified
        if start_date:
            df = df[df["timestamp"] >= start_date]
        if end_date:
            df = df[df["timestamp"] <= end_date]
        
        # Iterate through each time step
        for idx, row in df.iterrows():
            timestamp = row["timestamp"]
            self.timestamps.append(timestamp)
            
            # Prepare market data snapshot for this timestamp
            market_snapshot = self._prepare_market_snapshot(
                historical_data, timestamp
            )
            
            # Generate signal from strategy
            signal = await strategy.generate_signal(market_snapshot)
            
            # Execute signal if present
            if signal:
                self._execute_backtest_signal(signal, market_snapshot)
            
            # Update equity curve
            portfolio_value = self._calculate_portfolio_value(market_snapshot)
            self.equity_curve.append(portfolio_value)
        
        # Calculate performance metrics
        results = self._calculate_metrics()
        logger.info(f"Backtest completed. Final value: ${results['final_value']:.2f}")
        
        return results
    
    def _prepare_market_snapshot(
        self,
        historical_data: Dict[str, pd.DataFrame],
        timestamp: datetime
    ) -> Dict[str, Any]:
        """
        Prepare market data snapshot at a specific timestamp.
        
        Args:
            historical_data: Full historical data
            timestamp: Current timestamp
            
        Returns:
            Market snapshot dictionary
        """
        snapshot = {}
        
        for symbol, df in historical_data.items():
            # Get data up to current timestamp
            current_data = df[df["timestamp"] <= timestamp]
            
            if not current_data.empty:
                latest = current_data.iloc[-1]
                snapshot[symbol] = {
                    "ticker": {
                        "last": latest["close"],
                        "bid": latest["low"],
                        "ask": latest["high"],
                        "volume": latest["volume"]
                    },
                    "ohlcv": current_data
                }
        
        return snapshot
    
    def _execute_backtest_signal(
        self,
        signal: Dict[str, Any],
        market_data: Dict[str, Any]
    ) -> None:
        """
        Execute a trading signal in backtest.
        
        Args:
            signal: Signal dictionary
            market_data: Current market data
        """
        action = signal.get("action")
        symbol = signal.get("symbol")
        amount = signal.get("amount", 0)
        
        if symbol not in market_data:
            return
        
        price = market_data[symbol]["ticker"]["last"]
        
        if action == "buy":
            # Apply slippage (pay more)
            execution_price = price * (1 + self.slippage)
            cost = execution_price * amount
            commission_cost = cost * self.commission
            total_cost = cost + commission_cost
            
            if total_cost <= self.capital:
                self.capital -= total_cost
                self.positions[symbol] = self.positions.get(symbol, 0) + amount
                
                self.trades.append({
                    "timestamp": self.timestamps[-1],
                    "action": "buy",
                    "symbol": symbol,
                    "amount": amount,
                    "price": execution_price,
                    "cost": total_cost
                })
        
        elif action == "sell":
            # Apply slippage (receive less)
            execution_price = price * (1 - self.slippage)
            
            if symbol in self.positions and self.positions[symbol] >= amount:
                proceeds = execution_price * amount
                commission_cost = proceeds * self.commission
                net_proceeds = proceeds - commission_cost
                
                self.capital += net_proceeds
                self.positions[symbol] -= amount
                
                if self.positions[symbol] == 0:
                    del self.positions[symbol]
                
                self.trades.append({
                    "timestamp": self.timestamps[-1],
                    "action": "sell",
                    "symbol": symbol,
                    "amount": amount,
                    "price": execution_price,
                    "proceeds": net_proceeds
                })
    
    def _calculate_portfolio_value(self, market_data: Dict[str, Any]) -> float:
        """
        Calculate total portfolio value.
        
        Args:
            market_data: Current market data
            
        Returns:
            Total portfolio value
        """
        total_value = self.capital
        
        for symbol, amount in self.positions.items():
            if symbol in market_data:
                price = market_data[symbol]["ticker"]["last"]
                total_value += price * amount
        
        return total_value
    
    def _calculate_metrics(self) -> Dict[str, Any]:
        """
        Calculate performance metrics.
        
        Returns:
            Dictionary of performance metrics
        """
        equity_array = np.array(self.equity_curve)
        returns = np.diff(equity_array) / equity_array[:-1]
        
        # Basic metrics
        final_value = equity_array[-1]
        total_return = (final_value - self.initial_capital) / self.initial_capital
        
        # Risk metrics
        volatility = np.std(returns) * np.sqrt(252) if len(returns) > 0 else 0
        sharpe_ratio = (np.mean(returns) * 252 / volatility) if volatility > 0 else 0
        
        # Drawdown
        cumulative_max = np.maximum.accumulate(equity_array)
        drawdown = (equity_array - cumulative_max) / cumulative_max
        max_drawdown = np.min(drawdown)
        
        return {
            "initial_capital": self.initial_capital,
            "final_value": final_value,
            "total_return": total_return,
            "total_return_pct": total_return * 100,
            "num_trades": len(self.trades),
            "volatility": volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "max_drawdown_pct": max_drawdown * 100,
            "equity_curve": self.equity_curve,
            "timestamps": self.timestamps,
            "trades": self.trades
        }
    
    def get_results_dataframe(self) -> pd.DataFrame:
        """
        Get backtest results as a pandas DataFrame.
        
        Returns:
            DataFrame with equity curve and timestamps
        """
        return pd.DataFrame({
            "timestamp": self.timestamps,
            "equity": self.equity_curve[1:]  # Skip initial value
        })
