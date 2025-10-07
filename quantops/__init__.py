"""
QuantOps Engine - Algorithmic Liquidity & Quantitative Strategy Engine

Python-based quantitative trading engine powering Cryptobeam's liquidity algorithms.
Integrates with CCXT for multi-exchange execution, backtesting modules, and agent 
swarm AI models for autonomous market-making.
"""

__version__ = "0.1.0"
__author__ = "REDDNoC"

from quantops.core.engine import TradingEngine
from quantops.exchange.manager import ExchangeManager
from quantops.backtesting.backtester import Backtester
from quantops.models.agent_swarm import AgentSwarm

__all__ = [
    "TradingEngine",
    "ExchangeManager",
    "Backtester",
    "AgentSwarm",
]
