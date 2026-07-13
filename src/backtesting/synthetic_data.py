"""Synthetic realistic price data for backtesting when live data unavailable"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_synthetic_prices(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Generate realistic synthetic OHLCV data"""
    
    # Stock characteristics
    characteristics = {
        'AAPL': {'base': 150, 'volatility': 0.02, 'trend': 0.0005},
        'MSFT': {'base': 250, 'volatility': 0.018, 'trend': 0.0006},
        'GOOGL': {'base': 100, 'volatility': 0.019, 'trend': 0.0004},
        'AMZN': {'base': 130, 'volatility': 0.021, 'trend': 0.0003},
        'META': {'base': 200, 'volatility': 0.025, 'trend': 0.0002},
        'NVDA': {'base': 400, 'volatility': 0.03, 'trend': 0.001},
        'TSLA': {'base': 240, 'volatility': 0.035, 'trend': -0.0002},
    }
    
    if ticker not in characteristics:
        characteristics[ticker] = {'base': 100, 'volatility': 0.02, 'trend': 0.0004}
    
    char = characteristics[ticker]
    
    # Date range
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    dates = pd.bdate_range(start, end)
    
    np.random.seed(hash(ticker + start_date + end_date) % 2**32)
    
    prices = []
    current_price = char['base']
    
    for date in dates:
        # Geometric brownian motion
        drift = char['trend']
        shock = np.random.normal(0, char['volatility'])
        current_price = current_price * np.exp(drift + shock)
        
        # OHLC
        open_p = current_price
        high_p = current_price * (1 + abs(np.random.normal(0, char['volatility'] * 0.5)))
        low_p = current_price * (1 - abs(np.random.normal(0, char['volatility'] * 0.5)))
        close_p = current_price
        volume = int(np.random.normal(50000000, 10000000))
        
        prices.append({
            'Date': date,
            'Open': open_p,
            'High': high_p,
            'Low': low_p,
            'Close': close_p,
            'Volume': max(1000000, volume)
        })
    
    df = pd.DataFrame(prices)
    df.set_index('Date', inplace=True)
    
    return df
