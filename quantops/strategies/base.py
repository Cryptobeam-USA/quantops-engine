"""Base strategy class for implementing trading strategies."""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
import pandas as pd


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    
    All custom strategies should inherit from this class and implement
    the generate_signal method.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize strategy.
        
        Args:
            config: Strategy configuration dictionary
        """
        self.config = config
        self.name = config.get("name", self.__class__.__name__)
        self.symbols = config.get("symbols", [])
    
    @abstractmethod
    async def generate_signal(self, market_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate trading signal based on market data.
        
        Args:
            market_data: Dictionary containing market data (ticker, ohlcv, etc.)
            
        Returns:
            Signal dictionary with keys: action, symbol, amount, price
            Returns None if no signal
        """
        pass
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical indicators on OHLCV data.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with added indicator columns
        """
        return df
