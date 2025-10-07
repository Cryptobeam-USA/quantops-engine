"""Utility functions for technical analysis and data processing."""

import pandas as pd
import numpy as np
from typing import Optional


def calculate_sma(data: pd.Series, period: int) -> pd.Series:
    """
    Calculate Simple Moving Average.
    
    Args:
        data: Price data series
        period: Period for SMA calculation
        
    Returns:
        SMA series
    """
    return data.rolling(window=period).mean()


def calculate_ema(data: pd.Series, period: int) -> pd.Series:
    """
    Calculate Exponential Moving Average.
    
    Args:
        data: Price data series
        period: Period for EMA calculation
        
    Returns:
        EMA series
    """
    return data.ewm(span=period, adjust=False).mean()


def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate Relative Strength Index.
    
    Args:
        data: Price data series
        period: Period for RSI calculation
        
    Returns:
        RSI series
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(
    data: pd.Series,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9
) -> tuple:
    """
    Calculate MACD (Moving Average Convergence Divergence).
    
    Args:
        data: Price data series
        fast_period: Fast EMA period
        slow_period: Slow EMA period
        signal_period: Signal line EMA period
        
    Returns:
        Tuple of (macd, signal, histogram)
    """
    fast_ema = calculate_ema(data, fast_period)
    slow_ema = calculate_ema(data, slow_period)
    
    macd = fast_ema - slow_ema
    signal = calculate_ema(macd, signal_period)
    histogram = macd - signal
    
    return macd, signal, histogram


def calculate_bollinger_bands(
    data: pd.Series,
    period: int = 20,
    std_dev: float = 2.0
) -> tuple:
    """
    Calculate Bollinger Bands.
    
    Args:
        data: Price data series
        period: Period for moving average
        std_dev: Number of standard deviations
        
    Returns:
        Tuple of (upper_band, middle_band, lower_band)
    """
    middle_band = calculate_sma(data, period)
    std = data.rolling(window=period).std()
    
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    
    return upper_band, middle_band, lower_band


def calculate_atr(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 14
) -> pd.Series:
    """
    Calculate Average True Range.
    
    Args:
        high: High price series
        low: Low price series
        close: Close price series
        period: Period for ATR calculation
        
    Returns:
        ATR series
    """
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr


def normalize_data(data: pd.Series) -> pd.Series:
    """
    Normalize data to 0-1 range.
    
    Args:
        data: Data series to normalize
        
    Returns:
        Normalized series
    """
    min_val = data.min()
    max_val = data.max()
    
    if max_val == min_val:
        return pd.Series(0.5, index=data.index)
    
    return (data - min_val) / (max_val - min_val)


def calculate_returns(prices: pd.Series) -> pd.Series:
    """
    Calculate returns from price series.
    
    Args:
        prices: Price series
        
    Returns:
        Returns series
    """
    return prices.pct_change()


def calculate_volatility(returns: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculate rolling volatility.
    
    Args:
        returns: Returns series
        period: Period for volatility calculation
        
    Returns:
        Volatility series
    """
    return returns.rolling(window=period).std()
