import logging
from typing import List, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class SignalResult:
    """Result of a single signal validation"""
    headline: str
    ticker: str
    signal_date: str
    signal_direction: str
    signal_confidence: float
    guidance_direction: str
    entry_price: float
    exit_price: Optional[float]
    price_change: Optional[float]
    pnl: float
    is_profitable: bool
    holding_days: int
    reason: str


class SignalValidator:
    """Validate signals against real historical price data"""
    
    def __init__(self, data_loader, holding_period: int = 5):
        self.data_loader = data_loader
        self.holding_period = holding_period
        self.signal_results = []
    
    def validate_signals(self, headlines: List[Dict]) -> List[SignalResult]:
        """Run all headlines through validation against real prices"""
        
        print(f"\n🔬 Validating {len(headlines)} signals against real price data...\n")
        
        valid_signals = 0
        skipped_signals = 0
        
        for headline_data in headlines:
            headline = headline_data['headline']
            date = headline_data['date']
            ticker = headline_data['ticker']
            guidance_direction = headline_data['direction']
            
            entry_price = self.data_loader.get_price_at_date(ticker, date)
            exit_price = self.data_loader.get_price_after_days(ticker, date, self.holding_period)
            
            if not entry_price or not exit_price:
                skipped_signals += 1
                continue
            
            price_change = (exit_price - entry_price) / entry_price
            
            if guidance_direction == "raised":
                trade_signal = "long"
                pnl = price_change
                reason = f"Raised guidance - expected upside"
            elif guidance_direction == "lowered":
                trade_signal = "short"
                pnl = -price_change
                reason = f"Lowered guidance - expected downside"
            else:
                trade_signal = "neutral"
                pnl = 0
                reason = f"Neutral guidance - no trade"
            
            result = SignalResult(
                headline=headline,
                ticker=ticker,
                signal_date=date,
                signal_direction=trade_signal,
                signal_confidence=0.7 if trade_signal != "neutral" else 0.5,
                guidance_direction=guidance_direction,
                entry_price=entry_price,
                exit_price=exit_price,
                price_change=price_change,
                pnl=pnl,
                is_profitable=pnl > 0,
                holding_days=self.holding_period,
                reason=reason
            )
            
            self.signal_results.append(result)
            valid_signals += 1
            
            if trade_signal != "neutral":
                status = "✅" if result.is_profitable else "❌"
                print(f"{status} {ticker} | {date} | {trade_signal.upper():6} | Entry: ${entry_price:7.2f} | Exit: ${exit_price:7.2f} | P&L: {pnl:+.2%}")
        
        print(f"\n✅ Valid signals: {valid_signals} | Skipped: {skipped_signals}\n")
        
        return self.signal_results
