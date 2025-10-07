"""Unit tests for backtesting module."""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from quantops.backtesting.backtester import Backtester
from quantops.strategies.base import BaseStrategy


class SimpleStrategy(BaseStrategy):
    """Simple strategy for testing."""
    
    async def generate_signal(self, market_data):
        # Buy when price is below 45000
        if "BTC/USDT" in market_data:
            price = market_data["BTC/USDT"]["ticker"]["last"]
            if price < 45000:
                return {"action": "buy", "symbol": "BTC/USDT", "amount": 0.1}
        return None


@pytest.fixture
def backtester():
    """Create a backtester instance."""
    return Backtester(
        initial_capital=100000.0,
        commission=0.001,
        slippage=0.0005
    )


@pytest.fixture
def sample_data():
    """Generate sample historical data."""
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=100, freq='1H')
    
    return {
        "BTC/USDT": pd.DataFrame({
            "timestamp": dates,
            "open": 45000 + np.random.randn(100) * 100,
            "high": 46000 + np.random.randn(100) * 100,
            "low": 44000 + np.random.randn(100) * 100,
            "close": 45000 + np.random.randn(100) * 100,
            "volume": np.random.rand(100) * 1000000
        })
    }


def test_backtester_initialization(backtester):
    """Test backtester initialization."""
    assert backtester.initial_capital == 100000.0
    assert backtester.commission == 0.001
    assert backtester.slippage == 0.0005
    assert backtester.capital == 100000.0
    assert len(backtester.trades) == 0


def test_backtester_reset(backtester):
    """Test backtester reset."""
    backtester.capital = 50000.0
    backtester.trades = [{"test": "trade"}]
    
    backtester.reset()
    
    assert backtester.capital == 100000.0
    assert len(backtester.trades) == 0
    assert len(backtester.equity_curve) == 1


@pytest.mark.asyncio
async def test_backtest_run(backtester, sample_data):
    """Test running a backtest."""
    strategy = SimpleStrategy({"name": "test", "symbols": ["BTC/USDT"]})
    
    results = await backtester.run(strategy, sample_data)
    
    assert "initial_capital" in results
    assert "final_value" in results
    assert "total_return" in results
    assert "num_trades" in results
    assert "sharpe_ratio" in results
    assert "max_drawdown" in results
    
    assert results["initial_capital"] == 100000.0


def test_calculate_portfolio_value(backtester):
    """Test portfolio value calculation."""
    backtester.capital = 50000.0
    backtester.positions = {"BTC/USDT": 1.0}
    
    market_data = {
        "BTC/USDT": {
            "ticker": {"last": 50000.0}
        }
    }
    
    value = backtester._calculate_portfolio_value(market_data)
    assert value == 100000.0  # 50000 cash + 1 BTC * 50000


def test_results_dataframe(backtester):
    """Test getting results as dataframe."""
    backtester.timestamps = [datetime.now(), datetime.now()]
    backtester.equity_curve = [100000.0, 105000.0, 110000.0]
    
    df = backtester.get_results_dataframe()
    
    assert isinstance(df, pd.DataFrame)
    assert "timestamp" in df.columns
    assert "equity" in df.columns
    assert len(df) == 2
