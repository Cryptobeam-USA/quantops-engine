"""Example momentum-based trading strategy."""

from typing import Dict, Optional, Any
import pandas as pd

from quantops.strategies.base import BaseStrategy
from quantops.utils.indicators import calculate_rsi, calculate_macd


class MomentumStrategy(BaseStrategy):
    """
    Simple momentum-based trading strategy using RSI and MACD.
    
    Generates buy signals when:
    - RSI < 30 (oversold)
    - MACD crosses above signal line
    
    Generates sell signals when:
    - RSI > 70 (overbought)
    - MACD crosses below signal line
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize momentum strategy.
        
        Args:
            config: Strategy configuration
        """
        super().__init__(config)
        
        self.rsi_period = config.get("rsi_period", 14)
        self.rsi_oversold = config.get("rsi_oversold", 30)
        self.rsi_overbought = config.get("rsi_overbought", 70)
        self.position_size = config.get("position_size", 0.1)
    
    async def generate_signal(self, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate trading signal based on momentum indicators.
        
        Args:
            market_data: Dictionary containing market data
            
        Returns:
            Signal dictionary or None
        """
        for symbol in self.symbols:
            if symbol not in market_data:
                continue
            
            ohlcv = market_data[symbol].get("ohlcv")
            
            if not isinstance(ohlcv, pd.DataFrame) or len(ohlcv) < 50:
                continue
            
            # Calculate indicators
            df = self._add_indicators(ohlcv)
            
            if df is None or len(df) < 2:
                continue
            
            # Get latest values
            latest = df.iloc[-1]
            previous = df.iloc[-2]
            
            rsi = latest["rsi"]
            macd = latest["macd"]
            signal_line = latest["signal"]
            prev_macd = previous["macd"]
            prev_signal = previous["signal"]
            
            # Check for buy signal
            if (rsi < self.rsi_oversold and 
                macd > signal_line and 
                prev_macd <= prev_signal):
                
                return {
                    "action": "buy",
                    "symbol": symbol,
                    "amount": self.position_size,
                    "reason": f"RSI oversold ({rsi:.2f}) + MACD crossover"
                }
            
            # Check for sell signal
            if (rsi > self.rsi_overbought and 
                macd < signal_line and 
                prev_macd >= prev_signal):
                
                return {
                    "action": "sell",
                    "symbol": symbol,
                    "amount": self.position_size,
                    "reason": f"RSI overbought ({rsi:.2f}) + MACD crossunder"
                }
        
        return None
    
    def _add_indicators(self, df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """
        Add technical indicators to dataframe.
        
        Args:
            df: OHLCV dataframe
            
        Returns:
            DataFrame with indicators added
        """
        try:
            df = df.copy()
            
            # Calculate RSI
            df["rsi"] = calculate_rsi(df["close"], self.rsi_period)
            
            # Calculate MACD
            macd, signal, histogram = calculate_macd(df["close"])
            df["macd"] = macd
            df["signal"] = signal
            df["histogram"] = histogram
            
            # Drop NaN values
            df = df.dropna()
            
            return df
            
        except Exception as e:
            return None
