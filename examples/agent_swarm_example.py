"""Example: Using the AI agent swarm for signal evaluation."""

import asyncio
import logging

from quantops.models.agent_swarm import AgentSwarm, Agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting Agent Swarm example...")
    
    # Initialize agent swarm
    swarm = AgentSwarm({
        "consensus_threshold": 0.65,
        "agents": []
    })
    
    # Add custom agents
    trend_agent = Agent(
        name="trend_follower",
        agent_type="neural",
        config={"weight": 1.2, "input_dim": 10}
    )
    swarm.add_agent(trend_agent)
    
    momentum_agent = Agent(
        name="momentum_trader",
        agent_type="neural",
        config={"weight": 1.0, "input_dim": 10}
    )
    swarm.add_agent(momentum_agent)
    
    volatility_agent = Agent(
        name="volatility_analyzer",
        agent_type="rule_based",
        config={"weight": 0.8}
    )
    swarm.add_agent(volatility_agent)
    
    logger.info(f"Initialized swarm with {len(swarm.agents)} agents")
    
    # Create sample signals
    signals = [
        {
            "action": "buy",
            "symbol": "BTC/USDT",
            "amount": 0.1
        },
        {
            "action": "sell",
            "symbol": "ETH/USDT",
            "amount": 0.5
        },
        {
            "action": "buy",
            "symbol": "SOL/USDT",
            "amount": 10.0
        }
    ]
    
    # Sample market data
    market_data = {
        "BTC/USDT": {
            "ticker": {"last": 50000, "volume": 2000000},
            "ohlcv": None
        },
        "ETH/USDT": {
            "ticker": {"last": 3000, "volume": 5000000},
            "ohlcv": None
        },
        "SOL/USDT": {
            "ticker": {"last": 100, "volume": 1000000},
            "ohlcv": None
        }
    }
    
    # Process signals through swarm
    logger.info(f"\nProcessing {len(signals)} signals through agent swarm...")
    approved_signals = await swarm.process_signals(signals, market_data)
    
    # Display results
    logger.info(f"\nSwarm approved {len(approved_signals)} out of {len(signals)} signals:")
    for signal in approved_signals:
        logger.info(f"  ✓ {signal['action'].upper()} {signal['amount']} {signal['symbol']} "
                   f"(consensus: {signal['consensus_score']:.2f})")
    
    logger.info("\nAgent swarm example completed!")


if __name__ == "__main__":
    asyncio.run(main())
