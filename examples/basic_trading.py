"""Example: Basic trading engine usage."""

import asyncio
import logging
from quantops import TradingEngine
from quantops.strategies.momentum import MomentumStrategy
from quantops.config.settings import load_config, setup_logging


async def main():
    # Load and setup configuration
    config = load_config()
    setup_logging(config)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting QuantOps Engine example...")
    
    # Initialize trading engine
    engine = TradingEngine(config)
    
    # Create and add a momentum strategy
    strategy = MomentumStrategy({
        "name": "momentum_example",
        "symbols": ["BTC/USDT", "ETH/USDT"],
        "rsi_period": 14,
        "rsi_oversold": 30,
        "rsi_overbought": 70,
        "position_size": 0.05
    })
    
    engine.add_strategy(strategy)
    
    logger.info("Strategy added. Starting engine...")
    
    # Start the engine (this will run indefinitely)
    try:
        await engine.start()
    except KeyboardInterrupt:
        logger.info("Stopping engine...")
        await engine.stop()
        logger.info("Engine stopped successfully")


if __name__ == "__main__":
    asyncio.run(main())
