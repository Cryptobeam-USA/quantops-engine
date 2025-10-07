"""Core trading engine implementation."""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
import numpy as np

from quantops.exchange.manager import ExchangeManager
from quantops.strategies.base import BaseStrategy
from quantops.models.agent_swarm import AgentSwarm


logger = logging.getLogger(__name__)


class TradingEngine:
    """
    Main trading engine for executing quantitative strategies.
    
    Coordinates exchange connectivity, strategy execution, risk management,
    and AI agent swarm decision making.
    """
    
    def __init__(
        self,
        config: Dict[str, Any],
        exchange_manager: Optional[ExchangeManager] = None,
        agent_swarm: Optional[AgentSwarm] = None
    ):
        """
        Initialize the trading engine.
        
        Args:
            config: Configuration dictionary
            exchange_manager: Optional ExchangeManager instance
            agent_swarm: Optional AgentSwarm instance for AI-driven decisions
        """
        self.config = config
        self.exchange_manager = exchange_manager or ExchangeManager(config.get("exchanges", {}))
        self.agent_swarm = agent_swarm
        self.strategies: List[BaseStrategy] = []
        self.running = False
        self.positions: Dict[str, Any] = {}
        self.portfolio_value = config.get("initial_capital", 100000.0)
        
        logger.info("TradingEngine initialized with config: %s", config)
    
    def add_strategy(self, strategy: BaseStrategy) -> None:
        """
        Add a trading strategy to the engine.
        
        Args:
            strategy: Strategy instance to add
        """
        self.strategies.append(strategy)
        logger.info(f"Added strategy: {strategy.__class__.__name__}")
    
    async def start(self) -> None:
        """Start the trading engine."""
        self.running = True
        logger.info("Trading engine started")
        
        await self.exchange_manager.connect_all()
        
        # Main trading loop
        while self.running:
            try:
                await self._execute_trading_cycle()
                await asyncio.sleep(self.config.get("cycle_interval", 1.0))
            except Exception as e:
                logger.error(f"Error in trading cycle: {e}")
                if self.config.get("stop_on_error", False):
                    await self.stop()
    
    async def stop(self) -> None:
        """Stop the trading engine."""
        self.running = False
        await self.exchange_manager.disconnect_all()
        logger.info("Trading engine stopped")
    
    async def _execute_trading_cycle(self) -> None:
        """Execute one trading cycle."""
        # Fetch market data
        market_data = await self._fetch_market_data()
        
        # Generate signals from strategies
        signals = []
        for strategy in self.strategies:
            signal = await strategy.generate_signal(market_data)
            if signal:
                signals.append(signal)
        
        # Use AI agent swarm for decision making if available
        if self.agent_swarm and signals:
            signals = await self.agent_swarm.process_signals(signals, market_data)
        
        # Execute trades based on signals
        for signal in signals:
            await self._execute_signal(signal)
        
        # Update portfolio metrics
        await self._update_portfolio()
    
    async def _fetch_market_data(self) -> Dict[str, pd.DataFrame]:
        """
        Fetch current market data from exchanges.
        
        Returns:
            Dictionary of market data dataframes by symbol
        """
        market_data = {}
        symbols = self.config.get("symbols", [])
        
        for symbol in symbols:
            try:
                ticker = await self.exchange_manager.fetch_ticker(symbol)
                ohlcv = await self.exchange_manager.fetch_ohlcv(symbol)
                
                market_data[symbol] = {
                    "ticker": ticker,
                    "ohlcv": pd.DataFrame(
                        ohlcv,
                        columns=["timestamp", "open", "high", "low", "close", "volume"]
                    ) if ohlcv else pd.DataFrame()
                }
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {e}")
        
        return market_data
    
    async def _execute_signal(self, signal: Dict[str, Any]) -> None:
        """
        Execute a trading signal.
        
        Args:
            signal: Signal dictionary containing action, symbol, amount, etc.
        """
        try:
            action = signal.get("action")
            symbol = signal.get("symbol")
            amount = signal.get("amount")
            
            if action == "buy":
                order = await self.exchange_manager.create_market_buy_order(symbol, amount)
                logger.info(f"Executed BUY order: {order}")
            elif action == "sell":
                order = await self.exchange_manager.create_market_sell_order(symbol, amount)
                logger.info(f"Executed SELL order: {order}")
            
        except Exception as e:
            logger.error(f"Error executing signal {signal}: {e}")
    
    async def _update_portfolio(self) -> None:
        """Update portfolio positions and value."""
        try:
            balance = await self.exchange_manager.fetch_balance()
            self.positions = balance
            
            # Calculate total portfolio value
            total_value = 0.0
            for currency, amount in balance.items():
                if currency == "USDT" or currency == "USD":
                    total_value += amount
                else:
                    # Convert to USD equivalent (simplified)
                    ticker = await self.exchange_manager.fetch_ticker(f"{currency}/USDT")
                    if ticker:
                        total_value += amount * ticker.get("last", 0)
            
            self.portfolio_value = total_value
            logger.debug(f"Portfolio value updated: ${self.portfolio_value:.2f}")
            
        except Exception as e:
            logger.error(f"Error updating portfolio: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current engine status.
        
        Returns:
            Dictionary containing engine status information
        """
        return {
            "running": self.running,
            "strategies": len(self.strategies),
            "portfolio_value": self.portfolio_value,
            "positions": self.positions,
            "timestamp": datetime.utcnow().isoformat()
        }
