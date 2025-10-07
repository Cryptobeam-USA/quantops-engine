"""Unit tests for core trading engine."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch

from quantops.core.engine import TradingEngine
from quantops.strategies.base import BaseStrategy


class MockStrategy(BaseStrategy):
    """Mock strategy for testing."""
    
    async def generate_signal(self, market_data):
        return {
            "action": "buy",
            "symbol": "BTC/USDT",
            "amount": 0.1
        }


@pytest.fixture
def basic_config():
    """Basic configuration for testing."""
    return {
        "initial_capital": 100000.0,
        "cycle_interval": 1.0,
        "symbols": ["BTC/USDT"],
        "exchanges": {}
    }


@pytest.fixture
def trading_engine(basic_config):
    """Create a trading engine instance."""
    return TradingEngine(basic_config)


def test_engine_initialization(trading_engine, basic_config):
    """Test engine initialization."""
    assert trading_engine.config == basic_config
    assert trading_engine.running is False
    assert trading_engine.portfolio_value == basic_config["initial_capital"]
    assert len(trading_engine.strategies) == 0


def test_add_strategy(trading_engine):
    """Test adding a strategy."""
    strategy = MockStrategy({"name": "test", "symbols": ["BTC/USDT"]})
    trading_engine.add_strategy(strategy)
    
    assert len(trading_engine.strategies) == 1
    assert trading_engine.strategies[0] == strategy


def test_get_status(trading_engine):
    """Test getting engine status."""
    status = trading_engine.get_status()
    
    assert "running" in status
    assert "strategies" in status
    assert "portfolio_value" in status
    assert "positions" in status
    assert "timestamp" in status
    
    assert status["running"] is False
    assert status["strategies"] == 0
    assert status["portfolio_value"] == 100000.0


@pytest.mark.asyncio
async def test_engine_stop(trading_engine):
    """Test stopping the engine."""
    with patch.object(trading_engine.exchange_manager, 'disconnect_all', new_callable=AsyncMock):
        await trading_engine.stop()
        assert trading_engine.running is False
