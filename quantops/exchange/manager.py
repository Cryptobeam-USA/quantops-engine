"""Exchange manager for multi-exchange integration via CCXT."""

import logging
from typing import Dict, List, Optional, Any
import ccxt.async_support as ccxt
import asyncio

logger = logging.getLogger(__name__)


class ExchangeManager:
    """
    Manages connections to multiple cryptocurrency exchanges via CCXT.
    
    Provides unified interface for trading operations across different exchanges.
    """
    
    def __init__(self, config: Dict[str, Dict[str, Any]]):
        """
        Initialize exchange manager.
        
        Args:
            config: Dictionary of exchange configurations, keyed by exchange name
                   Example: {"binance": {"apiKey": "...", "secret": "..."}}
        """
        self.config = config
        self.exchanges: Dict[str, ccxt.Exchange] = {}
        self.default_exchange = None
        
        logger.info(f"ExchangeManager initialized with {len(config)} exchange(s)")
    
    async def connect_all(self) -> None:
        """Connect to all configured exchanges."""
        for exchange_name, exchange_config in self.config.items():
            await self.connect(exchange_name, exchange_config)
    
    async def connect(self, exchange_name: str, config: Dict[str, Any]) -> None:
        """
        Connect to a specific exchange.
        
        Args:
            exchange_name: Name of the exchange (e.g., 'binance', 'coinbase')
            config: Exchange-specific configuration
        """
        try:
            exchange_class = getattr(ccxt, exchange_name.lower())
            exchange = exchange_class(config)
            
            # Load markets
            await exchange.load_markets()
            
            self.exchanges[exchange_name] = exchange
            
            if self.default_exchange is None:
                self.default_exchange = exchange_name
            
            logger.info(f"Connected to {exchange_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to {exchange_name}: {e}")
            raise
    
    async def disconnect_all(self) -> None:
        """Disconnect from all exchanges."""
        for exchange_name, exchange in self.exchanges.items():
            try:
                await exchange.close()
                logger.info(f"Disconnected from {exchange_name}")
            except Exception as e:
                logger.error(f"Error disconnecting from {exchange_name}: {e}")
        
        self.exchanges.clear()
    
    def get_exchange(self, exchange_name: Optional[str] = None) -> ccxt.Exchange:
        """
        Get exchange instance.
        
        Args:
            exchange_name: Optional exchange name, uses default if not specified
            
        Returns:
            CCXT exchange instance
        """
        name = exchange_name or self.default_exchange
        if name not in self.exchanges:
            raise ValueError(f"Exchange {name} not connected")
        return self.exchanges[name]
    
    async def fetch_ticker(
        self, 
        symbol: str, 
        exchange_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch ticker data for a symbol.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTC/USDT')
            exchange_name: Optional exchange name
            
        Returns:
            Ticker data dictionary
        """
        exchange = self.get_exchange(exchange_name)
        return await exchange.fetch_ticker(symbol)
    
    async def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1m",
        limit: int = 100,
        exchange_name: Optional[str] = None
    ) -> List[List]:
        """
        Fetch OHLCV (candlestick) data.
        
        Args:
            symbol: Trading pair symbol
            timeframe: Timeframe (e.g., '1m', '5m', '1h', '1d')
            limit: Number of candles to fetch
            exchange_name: Optional exchange name
            
        Returns:
            List of OHLCV data
        """
        exchange = self.get_exchange(exchange_name)
        return await exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    
    async def fetch_order_book(
        self,
        symbol: str,
        limit: int = 20,
        exchange_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch order book data.
        
        Args:
            symbol: Trading pair symbol
            limit: Depth of order book
            exchange_name: Optional exchange name
            
        Returns:
            Order book dictionary with bids and asks
        """
        exchange = self.get_exchange(exchange_name)
        return await exchange.fetch_order_book(symbol, limit)
    
    async def fetch_balance(
        self, 
        exchange_name: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Fetch account balance.
        
        Args:
            exchange_name: Optional exchange name
            
        Returns:
            Dictionary of balances by currency
        """
        exchange = self.get_exchange(exchange_name)
        balance = await exchange.fetch_balance()
        return balance.get("free", {})
    
    async def create_market_buy_order(
        self,
        symbol: str,
        amount: float,
        exchange_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a market buy order.
        
        Args:
            symbol: Trading pair symbol
            amount: Amount to buy
            exchange_name: Optional exchange name
            
        Returns:
            Order information dictionary
        """
        exchange = self.get_exchange(exchange_name)
        return await exchange.create_market_buy_order(symbol, amount)
    
    async def create_market_sell_order(
        self,
        symbol: str,
        amount: float,
        exchange_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a market sell order.
        
        Args:
            symbol: Trading pair symbol
            amount: Amount to sell
            exchange_name: Optional exchange name
            
        Returns:
            Order information dictionary
        """
        exchange = self.get_exchange(exchange_name)
        return await exchange.create_market_sell_order(symbol, amount)
    
    async def create_limit_buy_order(
        self,
        symbol: str,
        amount: float,
        price: float,
        exchange_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a limit buy order.
        
        Args:
            symbol: Trading pair symbol
            amount: Amount to buy
            price: Limit price
            exchange_name: Optional exchange name
            
        Returns:
            Order information dictionary
        """
        exchange = self.get_exchange(exchange_name)
        return await exchange.create_limit_buy_order(symbol, amount, price)
    
    async def create_limit_sell_order(
        self,
        symbol: str,
        amount: float,
        price: float,
        exchange_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a limit sell order.
        
        Args:
            symbol: Trading pair symbol
            amount: Amount to sell
            price: Limit price
            exchange_name: Optional exchange name
            
        Returns:
            Order information dictionary
        """
        exchange = self.get_exchange(exchange_name)
        return await exchange.create_limit_sell_order(symbol, amount, price)
    
    async def cancel_order(
        self,
        order_id: str,
        symbol: str,
        exchange_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cancel an order.
        
        Args:
            order_id: Order ID to cancel
            symbol: Trading pair symbol
            exchange_name: Optional exchange name
            
        Returns:
            Cancellation result dictionary
        """
        exchange = self.get_exchange(exchange_name)
        return await exchange.cancel_order(order_id, symbol)
    
    async def fetch_open_orders(
        self,
        symbol: Optional[str] = None,
        exchange_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch open orders.
        
        Args:
            symbol: Optional trading pair symbol (None for all symbols)
            exchange_name: Optional exchange name
            
        Returns:
            List of open orders
        """
        exchange = self.get_exchange(exchange_name)
        return await exchange.fetch_open_orders(symbol)
