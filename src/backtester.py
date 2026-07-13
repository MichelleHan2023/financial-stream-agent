import pandas as pd
import yfinance as yf
import logging
from typing import List, Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class Backtester:
    def __init__(self, initial_capital: float = 10000):
        """
        Initialize backtester
        
        Args:
            initial_capital: Starting portfolio value in USD
        """
        self.initial_capital = initial_capital
        self.portfolio_value = initial_capital
        self.positions = {}  # {ticker: quantity}
        self.trades = []  # History of all trades
        self.portfolio_history = []
        
    def fetch_historical_data(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """
        Fetch historical price data for a ticker
        
        Args:
            ticker: Stock ticker symbol
            period: Time period (e.g., "1y", "6mo", "3mo")
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            data = yf.download(ticker, period=period, progress=False)
            logger.info(f"Downloaded {len(data)} days of data for {ticker}")
            return data
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            return pd.DataFrame()
    
    def calculate_entry_price(self, ticker: str, signal_date: datetime) -> float:
        """
        Get the closing price on signal date (entry price)
        
        Args:
            ticker: Stock ticker
            signal_date: Date of signal
            
        Returns:
            Entry price or None if data not available
        """
        try:
            hist = yf.download(ticker, start=signal_date - timedelta(days=5), 
                              end=signal_date + timedelta(days=1), progress=False)
            if signal_date.date() in hist.index.date:
                return hist.loc[signal_date.date(), 'Close']
            elif len(hist) > 0:
                return hist['Close'].iloc[-1]
        except Exception as e:
            logger.error(f"Error getting entry price for {ticker}: {e}")
        
        return None
    
    def execute_signal(self, signal: Dict, current_date: datetime, 
                      position_size: float = 0.1):
        """
        Execute a trading signal
        
        Args:
            signal: Signal dict with ticker, direction, confidence
            current_date: Date of signal
            position_size: % of portfolio to allocate (0-1)
            
        Returns:
            Trade execution result
        """
        ticker = signal.get("ticker")
        direction = signal.get("guidance_direction")
        confidence = signal.get("guidance_confidence", 0.5)
        
        if not ticker or direction == "unknown":
            return {"status": "rejected", "reason": "Invalid signal"}
        
        entry_price = self.calculate_entry_price(ticker, current_date)
        if not entry_price:
            return {"status": "rejected", "reason": "Price data unavailable"}
        
        # Position sizing based on confidence
        allocation = self.portfolio_value * position_size * confidence
        quantity = int(allocation / entry_price)
        
        if quantity == 0:
            return {"status": "rejected", "reason": "Insufficient capital"}
        
        # Execute trade
        if direction == "raised":
            action = "BUY"
            self.positions[ticker] = self.positions.get(ticker, 0) + quantity
            self.portfolio_value -= quantity * entry_price
        elif direction == "lowered":
            action = "SELL"
            if ticker in self.positions:
                quantity = min(quantity, self.positions[ticker])
                self.positions[ticker] -= quantity
                self.portfolio_value += quantity * entry_price
            else:
                return {"status": "rejected", "reason": "No position to sell"}
        
        trade = {
            "date": current_date,
            "ticker": ticker,
            "action": action,
            "quantity": quantity,
            "price": entry_price,
            "value": quantity * entry_price,
            "confidence": confidence
        }
        
        self.trades.append(trade)
        logger.info(f"Executed {action} signal: {quantity} x {ticker} @ ${entry_price:.2f}")
        
        return {"status": "executed", "trade": trade}
    
    def calculate_pnl(self) -> Dict:
        """
        Calculate current P&L
        
        Returns:
            {
                "total_value": float,
                "total_pnl": float,
                "pnl_percent": float,
                "num_trades": int
            }
        """
        current_value = self.portfolio_value
        
        # Add current position values (using latest prices)
        for ticker, quantity in self.positions.items():
            try:
                latest_price = yf.download(ticker, period="1d", progress=False)['Close'].iloc[-1]
                current_value += quantity * latest_price
            except:
                pass
        
        total_pnl = current_value - self.initial_capital
        pnl_percent = (total_pnl / self.initial_capital) * 100 if self.initial_capital > 0 else 0
        
        return {
            "total_value": round(current_value, 2),
            "total_pnl": round(total_pnl, 2),
            "pnl_percent": round(pnl_percent, 2),
            "num_trades": len(self.trades)
        }
    
    def get_trade_history(self) -> List[Dict]:
        """Return all executed trades"""
        return self.trades