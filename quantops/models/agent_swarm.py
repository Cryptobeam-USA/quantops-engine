"""Agent swarm AI models for autonomous market-making and decision optimization."""

import logging
from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd

try:
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    logging.warning("TensorFlow not available. AI features will be limited.")

logger = logging.getLogger(__name__)


class Agent:
    """
    Individual AI agent for making trading decisions.
    
    Each agent specializes in different market aspects (trend, volatility, momentum, etc.)
    """
    
    def __init__(
        self,
        name: str,
        agent_type: str = "neural",
        config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize an agent.
        
        Args:
            name: Agent name
            agent_type: Type of agent (neural, rule_based, hybrid)
            config: Agent configuration
        """
        self.name = name
        self.agent_type = agent_type
        self.config = config or {}
        self.model = None
        self.weight = self.config.get("weight", 1.0)
        
        if agent_type == "neural" and TF_AVAILABLE:
            self._build_neural_model()
        
        logger.info(f"Agent '{name}' initialized (type: {agent_type})")
    
    def _build_neural_model(self) -> None:
        """Build a simple neural network model for the agent."""
        if not TF_AVAILABLE:
            return
        
        input_dim = self.config.get("input_dim", 10)
        
        self.model = keras.Sequential([
            keras.layers.Dense(64, activation="relu", input_shape=(input_dim,)),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation="relu"),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(16, activation="relu"),
            keras.layers.Dense(3, activation="softmax")  # buy, hold, sell
        ])
        
        self.model.compile(
            optimizer="adam",
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )
    
    async def evaluate_signal(
        self,
        signal: Dict[str, Any],
        market_data: Dict[str, Any]
    ) -> float:
        """
        Evaluate a trading signal and return confidence score.
        
        Args:
            signal: Trading signal to evaluate
            market_data: Current market data
            
        Returns:
            Confidence score between 0 and 1
        """
        if self.agent_type == "neural" and self.model and TF_AVAILABLE:
            return await self._neural_evaluation(signal, market_data)
        else:
            return await self._rule_based_evaluation(signal, market_data)
    
    async def _neural_evaluation(
        self,
        signal: Dict[str, Any],
        market_data: Dict[str, Any]
    ) -> float:
        """Neural network based evaluation."""
        # Extract features from market data
        features = self._extract_features(signal, market_data)
        
        if features is None:
            return 0.5  # Neutral
        
        # Get model prediction
        prediction = self.model.predict(features.reshape(1, -1), verbose=0)
        
        # Map prediction to confidence based on signal action
        action = signal.get("action")
        if action == "buy":
            confidence = prediction[0][0]  # Buy probability
        elif action == "sell":
            confidence = prediction[0][2]  # Sell probability
        else:
            confidence = prediction[0][1]  # Hold probability
        
        return float(confidence)
    
    async def _rule_based_evaluation(
        self,
        signal: Dict[str, Any],
        market_data: Dict[str, Any]
    ) -> float:
        """Rule-based evaluation (fallback)."""
        # Simple rule-based evaluation
        symbol = signal.get("symbol")
        if symbol not in market_data:
            return 0.5
        
        ticker = market_data[symbol].get("ticker", {})
        volume = ticker.get("volume", 0)
        
        # Higher volume = higher confidence
        confidence = min(volume / 1000000, 1.0) if volume > 0 else 0.5
        
        return confidence
    
    def _extract_features(
        self,
        signal: Dict[str, Any],
        market_data: Dict[str, Any]
    ) -> Optional[np.ndarray]:
        """
        Extract features from signal and market data.
        
        Args:
            signal: Trading signal
            market_data: Market data
            
        Returns:
            Feature array or None
        """
        symbol = signal.get("symbol")
        if symbol not in market_data:
            return None
        
        ticker = market_data[symbol].get("ticker", {})
        ohlcv = market_data[symbol].get("ohlcv")
        
        # Extract basic features
        features = []
        features.append(ticker.get("last", 0))
        features.append(ticker.get("volume", 0))
        features.append(signal.get("amount", 0))
        
        # Add technical indicators if OHLCV data available
        if isinstance(ohlcv, pd.DataFrame) and len(ohlcv) > 0:
            recent = ohlcv.tail(20)
            if len(recent) > 0:
                features.append(recent["close"].mean())
                features.append(recent["close"].std())
                features.append(recent["volume"].mean())
                features.append(recent["high"].max())
                features.append(recent["low"].min())
        
        # Pad to expected input dimension
        input_dim = self.config.get("input_dim", 10)
        while len(features) < input_dim:
            features.append(0.0)
        
        return np.array(features[:input_dim])


class AgentSwarm:
    """
    Swarm of AI agents that collectively make trading decisions.
    
    Implements consensus-based decision making where multiple agents
    evaluate signals and vote on the best course of action.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize agent swarm.
        
        Args:
            config: Swarm configuration
        """
        self.config = config or {}
        self.agents: List[Agent] = []
        self.consensus_threshold = self.config.get("consensus_threshold", 0.6)
        
        # Create default agents if none configured
        self._initialize_default_agents()
        
        logger.info(f"AgentSwarm initialized with {len(self.agents)} agents")
    
    def _initialize_default_agents(self) -> None:
        """Initialize default agent set."""
        agent_configs = self.config.get("agents", [])
        
        if not agent_configs:
            # Create default agents
            agent_configs = [
                {"name": "trend_agent", "type": "neural", "weight": 1.2},
                {"name": "momentum_agent", "type": "neural", "weight": 1.0},
                {"name": "volatility_agent", "type": "neural", "weight": 0.8},
                {"name": "volume_agent", "type": "rule_based", "weight": 0.7},
            ]
        
        for agent_config in agent_configs:
            agent = Agent(
                name=agent_config.get("name", "agent"),
                agent_type=agent_config.get("type", "neural"),
                config=agent_config
            )
            self.agents.append(agent)
    
    def add_agent(self, agent: Agent) -> None:
        """
        Add an agent to the swarm.
        
        Args:
            agent: Agent instance to add
        """
        self.agents.append(agent)
        logger.info(f"Added agent '{agent.name}' to swarm")
    
    async def process_signals(
        self,
        signals: List[Dict[str, Any]],
        market_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Process trading signals through agent swarm consensus.
        
        Args:
            signals: List of trading signals
            market_data: Current market data
            
        Returns:
            Filtered and ranked list of signals approved by swarm
        """
        approved_signals = []
        
        for signal in signals:
            # Get evaluations from all agents
            evaluations = []
            for agent in self.agents:
                score = await agent.evaluate_signal(signal, market_data)
                evaluations.append(score * agent.weight)
            
            # Calculate weighted consensus
            if evaluations:
                consensus = sum(evaluations) / sum(agent.weight for agent in self.agents)
                
                # Accept signal if consensus exceeds threshold
                if consensus >= self.consensus_threshold:
                    signal["consensus_score"] = consensus
                    approved_signals.append(signal)
                    logger.info(
                        f"Signal approved by swarm: {signal['action']} "
                        f"{signal['symbol']} (consensus: {consensus:.2f})"
                    )
        
        # Sort by consensus score (highest first)
        approved_signals.sort(key=lambda x: x.get("consensus_score", 0), reverse=True)
        
        return approved_signals
    
    async def train_agents(
        self,
        training_data: List[Dict[str, Any]],
        labels: List[int]
    ) -> None:
        """
        Train neural agents on historical data.
        
        Args:
            training_data: List of feature dictionaries
            labels: List of labels (0=sell, 1=hold, 2=buy)
        """
        if not TF_AVAILABLE:
            logger.warning("TensorFlow not available. Cannot train agents.")
            return
        
        for agent in self.agents:
            if agent.agent_type == "neural" and agent.model:
                # Extract features
                X = []
                for data in training_data:
                    features = agent._extract_features(data, {})
                    if features is not None:
                        X.append(features)
                
                X = np.array(X)
                y = keras.utils.to_categorical(labels, num_classes=3)
                
                # Train model
                agent.model.fit(
                    X, y,
                    epochs=10,
                    batch_size=32,
                    validation_split=0.2,
                    verbose=0
                )
                
                logger.info(f"Trained agent '{agent.name}'")
