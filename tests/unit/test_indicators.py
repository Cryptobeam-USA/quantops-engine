"""Unit tests for technical indicators."""

import pytest
import pandas as pd
import numpy as np

from quantops.utils.indicators import (
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
    normalize_data,
    calculate_returns
)


@pytest.fixture
def sample_prices():
    """Generate sample price data."""
    np.random.seed(42)
    return pd.Series(100 + np.cumsum(np.random.randn(100)))


def test_calculate_sma(sample_prices):
    """Test SMA calculation."""
    sma = calculate_sma(sample_prices, period=10)
    
    assert isinstance(sma, pd.Series)
    assert len(sma) == len(sample_prices)
    assert pd.isna(sma.iloc[0:9]).all()  # First 9 values should be NaN
    assert not pd.isna(sma.iloc[9])  # 10th value should not be NaN


def test_calculate_ema(sample_prices):
    """Test EMA calculation."""
    ema = calculate_ema(sample_prices, period=10)
    
    assert isinstance(ema, pd.Series)
    assert len(ema) == len(sample_prices)
    assert not pd.isna(ema.iloc[-1])


def test_calculate_rsi(sample_prices):
    """Test RSI calculation."""
    rsi = calculate_rsi(sample_prices, period=14)
    
    assert isinstance(rsi, pd.Series)
    assert len(rsi) == len(sample_prices)
    
    # RSI should be between 0 and 100
    valid_rsi = rsi.dropna()
    assert (valid_rsi >= 0).all()
    assert (valid_rsi <= 100).all()


def test_calculate_macd(sample_prices):
    """Test MACD calculation."""
    macd, signal, histogram = calculate_macd(sample_prices)
    
    assert isinstance(macd, pd.Series)
    assert isinstance(signal, pd.Series)
    assert isinstance(histogram, pd.Series)
    
    assert len(macd) == len(sample_prices)
    assert len(signal) == len(sample_prices)
    assert len(histogram) == len(sample_prices)


def test_calculate_bollinger_bands(sample_prices):
    """Test Bollinger Bands calculation."""
    upper, middle, lower = calculate_bollinger_bands(sample_prices, period=20)
    
    assert isinstance(upper, pd.Series)
    assert isinstance(middle, pd.Series)
    assert isinstance(lower, pd.Series)
    
    # Upper should be greater than middle, middle greater than lower
    valid_idx = middle.notna()
    assert (upper[valid_idx] >= middle[valid_idx]).all()
    assert (middle[valid_idx] >= lower[valid_idx]).all()


def test_normalize_data(sample_prices):
    """Test data normalization."""
    normalized = normalize_data(sample_prices)
    
    assert isinstance(normalized, pd.Series)
    assert len(normalized) == len(sample_prices)
    
    # Values should be between 0 and 1
    assert (normalized >= 0).all()
    assert (normalized <= 1).all()
    
    # Min should be 0, max should be 1
    assert normalized.min() == 0
    assert normalized.max() == 1


def test_calculate_returns(sample_prices):
    """Test returns calculation."""
    returns = calculate_returns(sample_prices)
    
    assert isinstance(returns, pd.Series)
    assert len(returns) == len(sample_prices)
    assert pd.isna(returns.iloc[0])  # First return should be NaN
