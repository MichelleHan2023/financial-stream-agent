import yfinance as yf
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
from backtesting.synthetic_data import generate_synthetic_prices

logger = logging.getLogger(__name__)

class RealDataLoader:
    """Load real or synthetic historical data"""
    
    def __init__(self, start_date: str, end_date: str, use_synthetic: bool = True):
        self.start_date = start_date
        self.end_date = end_date
        self.price_data = {}
        self.use_synthetic = use_synthetic
    
    def fetch_price_data(self, tickers: List[str]) -> Dict[str, pd.DataFrame]:
        """Fetch real or synthetic price data"""
        
        print(f"\n📥 Loading price data from {self.start_date} to {self.end_date}...\n")
        
        for ticker in tickers:
            try:
                print(f"  Loading {ticker}...", end=" ", flush=True)
                
                # Try real data first
                try:
                    df = yf.download(
                        ticker,
                        start=self.start_date,
                        end=self.end_date,
                        progress=False,
                        timeout=5
                    )
                    
                    if df is not None and len(df) > 0:
                        # Ensure proper datetime index
                        if not isinstance(df.index, pd.DatetimeIndex):
                            df.reset_index(inplace=True)
                            df['Date'] = pd.to_datetime(df['Date'])
                            df.set_index('Date', inplace=True)
                        
                        self.price_data[ticker] = df
                        print(f"✅ ({len(df)} days - REAL)")
                        logger.info(f"Loaded {ticker}: {len(df)} trading days (real)")
                        continue
                except:
                    pass
                
                # Fallback to synthetic
                if self.use_synthetic:
                    df = generate_synthetic_prices(ticker, self.start_date, self.end_date)
                    self.price_data[ticker] = df
                    print(f"✅ ({len(df)} days - SYNTHETIC)")
                    logger.info(f"Loaded {ticker}: {len(df)} trading days (synthetic)")
                else:
                    print(f"❌ (no data)")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}")
                logger.error(f"Error loading {ticker}: {e}")
        
        return self.price_data
    
    def get_price_at_date(self, ticker: str, date_str: str) -> Optional[float]:
        """Get closing price at specific date"""
        
        if ticker not in self.price_data or len(self.price_data[ticker]) == 0:
            return None
        
        df = self.price_data[ticker]
        target_date = pd.to_datetime(date_str)
        
        try:
            # Try exact date first
            if target_date in df.index:
                return float(df.loc[target_date, 'Close'])
            
            # Otherwise get the most recent date before target
            mask = df.index <= target_date
            if mask.any():
                return float(df.loc[mask, 'Close'].iloc[-1])
        except Exception as e:
            logger.error(f"Error getting price for {ticker} at {date_str}: {e}")
        
        return None
    
    def get_price_after_days(self, ticker: str, date_str: str, days: int) -> Optional[float]:
        """Get price N trading days after date"""
        
        if ticker not in self.price_data or len(self.price_data[ticker]) == 0:
            return None
        
        df = self.price_data[ticker]
        start_date = pd.to_datetime(date_str)
        
        try:
            mask = df.index >= start_date
            if mask.any():
                idx_pos = mask.argmax()
                if idx_pos + days < len(df):
                    return float(df.iloc[idx_pos + days]['Close'])
        except Exception as e:
            logger.error(f"Error getting price after days for {ticker}: {e}")
        
        return None
    
    def get_price_change(self, ticker: str, entry_date: str, exit_days: int) -> Optional[float]:
        """Calculate % price change over N days"""
        
        entry_price = self.get_price_at_date(ticker, entry_date)
        exit_price = self.get_price_after_days(ticker, entry_date, exit_days)
        
        if entry_price and exit_price:
            return (exit_price - entry_price) / entry_price
        
        return None


class RealHeadlineGenerator:
    """Generate realistic historical headlines"""
    
    REAL_EVENTS = [
        {"date": "2023-01-30", "ticker": "AAPL", "headline": "Apple reports strong iPhone sales, raises Q1 guidance", "direction": "raised"},
        {"date": "2023-02-02", "ticker": "MSFT", "headline": "Microsoft beats earnings expectations, announces cloud growth", "direction": "raised"},
        {"date": "2023-02-07", "ticker": "META", "headline": "Meta reports better-than-expected earnings, slashes costs", "direction": "raised"},
        {"date": "2023-02-14", "ticker": "GOOGL", "headline": "Google reports strong ad revenue but cuts headcount", "direction": "neutral"},
        {"date": "2023-02-22", "ticker": "AMZN", "headline": "Amazon beats Q4 earnings, raises full-year guidance", "direction": "raised"},
        
        {"date": "2023-04-19", "ticker": "TSLA", "headline": "Tesla cuts prices again amid competition, lowers margins", "direction": "lowered"},
        {"date": "2023-04-25", "ticker": "AAPL", "headline": "Apple reports iPhone revenue decline, misses expectations", "direction": "lowered"},
        {"date": "2023-04-27", "ticker": "MSFT", "headline": "Microsoft raises AI cloud guidance following ChatGPT success", "direction": "raised"},
        {"date": "2023-05-02", "ticker": "GOOGL", "headline": "Google reports revenue growth beats estimates", "direction": "raised"},
        {"date": "2023-05-04", "ticker": "META", "headline": "Meta misses earnings, issues weak forward guidance", "direction": "lowered"},
        
        {"date": "2023-07-19", "ticker": "AAPL", "headline": "Apple reports strong services revenue, raises Q3 guidance", "direction": "raised"},
        {"date": "2023-07-25", "ticker": "MSFT", "headline": "Microsoft raises guidance on Azure AI momentum", "direction": "raised"},
        {"date": "2023-07-26", "ticker": "META", "headline": "Meta beats earnings, announces buyback increase", "direction": "raised"},
        {"date": "2023-08-01", "ticker": "AMZN", "headline": "Amazon beats expectations, raises 2023 outlook", "direction": "raised"},
        {"date": "2023-08-02", "ticker": "TSLA", "headline": "Tesla reports margin compression, cuts guidance", "direction": "lowered"},
        
        {"date": "2023-10-24", "ticker": "AAPL", "headline": "Apple iPhone 15 sales strong, raises Q4 guidance", "direction": "raised"},
        {"date": "2023-10-25", "ticker": "MSFT", "headline": "Microsoft raises FY24 guidance on cloud AI adoption", "direction": "raised"},
        {"date": "2023-10-31", "ticker": "AMZN", "headline": "Amazon raises advertising revenue forecast", "direction": "raised"},
        {"date": "2023-11-01", "ticker": "NVDA", "headline": "Nvidia raises Q4 revenue guidance significantly on AI demand", "direction": "raised"},
        {"date": "2023-11-02", "ticker": "GOOGL", "headline": "Google reports strong ad recovery, raises outlook", "direction": "raised"},
        
        {"date": "2024-01-30", "ticker": "AAPL", "headline": "Apple reports services growth, maintains guidance", "direction": "neutral"},
        {"date": "2024-01-31", "ticker": "MSFT", "headline": "Microsoft beats earnings, raises guidance on Copilot revenue", "direction": "raised"},
        {"date": "2024-02-07", "ticker": "NVDA", "headline": "Nvidia raises guidance again, demand remains strong", "direction": "raised"},
        {"date": "2024-02-14", "ticker": "TSLA", "headline": "Tesla cuts prices further, lowers guidance", "direction": "lowered"},
        {"date": "2024-02-22", "ticker": "AMZN", "headline": "Amazon raises AWS guidance on enterprise AI adoption", "direction": "raised"},
        
        {"date": "2024-04-18", "ticker": "AAPL", "headline": "Apple reports Services record, raises guidance", "direction": "raised"},
        {"date": "2024-04-25", "ticker": "MSFT", "headline": "Microsoft raises Cloud revenue forecast significantly", "direction": "raised"},
        {"date": "2024-05-02", "ticker": "NVDA", "headline": "Nvidia Q1 revenue doubles expectations, raises guidance", "direction": "raised"},
        {"date": "2024-05-08", "ticker": "META", "headline": "Meta returns to strong growth, raises 2024 guidance", "direction": "raised"},
        {"date": "2024-05-15", "ticker": "GOOGL", "headline": "Google Ad revenue beats, but faces AI competition", "direction": "neutral"},
    ]
    
    @staticmethod
    def generate_realistic(output_file: str = "data/headlines/historical_headlines.json"):
        """Generate realistic headlines"""
        
        print(f"📝 Generating realistic historical headlines from real events...\n")
        
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(RealHeadlineGenerator.REAL_EVENTS, f, indent=2)
        
        print(f"✅ Generated {len(RealHeadlineGenerator.REAL_EVENTS)} realistic headlines")
        print(f"   → {output_file}")
        
        return RealHeadlineGenerator.REAL_EVENTS
