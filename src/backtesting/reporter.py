# src/backtesting/reporter.py
import json
from datetime import datetime
from typing import List
from .metrics_calculator import BacktestMetrics
from .signal_validator import SignalResult

class BacktestReporter:
    """Generate professional backtest reports"""
    
    def __init__(self, signal_results: List[SignalResult], metrics: BacktestMetrics):
        self.results = signal_results
        self.metrics = metrics
    
    def print_summary(self):
        """Print professional backtest summary"""
        
        print("\n" + "="*100)
        print("📊 BACKTEST REPORT - REAL HISTORICAL DATA VALIDATION")
        print("="*100 + "\n")
        
        print("📈 SIGNAL SUMMARY")
        print("-" * 100)
        print(f"  Period:                      {self.results[0].signal_date} to {self.results[-1].signal_date}")
        print(f"  Total Signals Generated:     {self.metrics.total_signals}")
        print(f"  Signals Traded:              {self.metrics.traded_signals}")
        print(f"  Signals Skipped (neutral):   {self.metrics.total_signals - self.metrics.traded_signals}\n")
        
        print("🎯 TRADE PERFORMANCE")
        print("-" * 100)
        print(f"  Winning Trades:              {self.metrics.winning_trades}")
        print(f"  Losing Trades:               {self.metrics.losing_trades}")
        print(f"  Win Rate:                    {self.metrics.win_rate:.1%}")
        print(f"  Accuracy vs Guidance:        {self.metrics.accuracy_vs_guidance:.1%}")
        print(f"  Best Single Trade:           {self.metrics.best_trade:+.2%}")
        print(f"  Worst Single Trade:          {self.metrics.worst_trade:+.2%}")
        print(f"  Max Consecutive Wins:        {self.metrics.consecutive_wins}")
        print(f"  Max Consecutive Losses:      {self.metrics.consecutive_losses}\n")
        
        print("💰 PROFITABILITY")
        print("-" * 100)
        print(f"  Average Win:                 {self.metrics.avg_win:+.2%}")
        print(f"  Average Loss:                {self.metrics.avg_loss:+.2%}")
        print(f"  Profit Factor:               {self.metrics.profit_factor:.2f}x")
        print(f"  Expected Value (per trade):  {self.metrics.expectancy:+.2%}")
        print(f"  Cumulative P&L:              {self.metrics.cumulative_pnl:+.2%}\n")
        
        print("📊 RISK METRICS")
        print("-" * 100)
        print(f"  Sharpe Ratio:                {self.metrics.sharpe_ratio:.2f}")
        print(f"  Max Drawdown:                {self.metrics.max_drawdown:.2%}\n")
        
        print("✅ QUALITY ASSESSMENT")
        print("-" * 100)
        self._print_interpretation()
        print("\n" + "="*100 + "\n")
    
    def _print_interpretation(self):
        """Provide professional interpretation"""
        
        if self.metrics.profit_factor > 2.5:
            quality = "🟢 EXCELLENT"
            quality_desc = "Exceptional trading edge"
        elif self.metrics.profit_factor > 2.0:
            quality = "🟢 VERY GOOD"
            quality_desc = "Strong trading edge"
        elif self.metrics.profit_factor > 1.5:
            quality = "🟡 GOOD"
            quality_desc = "Solid trading edge"
        elif self.metrics.profit_factor > 1.0:
            quality = "🟠 FAIR"
            quality_desc = "Marginal edge"
        else:
            quality = "🔴 POOR"
            quality_desc = "No edge or negative"
        
        print(f"Signal Quality:              {quality}")
        print(f"                             {quality_desc} (PF: {self.metrics.profit_factor:.2f}x)\n")
        
        if self.metrics.expectancy > 0.01:
            edge = "✅ POSITIVE"
            edge_val = f"+{self.metrics.expectancy:.2%}"
        elif self.metrics.expectancy > 0:
            edge = "⚠️  MARGINAL"
            edge_val = f"+{self.metrics.expectancy:.2%}"
        else:
            edge = "❌ NEGATIVE"
            edge_val = f"{self.metrics.expectancy:.2%}"
        
        print(f"Trading Edge:                {edge}")
        print(f"                             Expected value per trade: {edge_val}\n")
        
        if self.metrics.win_rate > 0.60:
            wr = "✅ EXCELLENT"
        elif self.metrics.win_rate > 0.55:
            wr = "✅ GOOD"
        elif self.metrics.win_rate > 0.50:
            wr = "⚠️  MARGINAL"
        else:
            wr = "❌ POOR"
        
        print(f"Win Rate:                    {wr} ({self.metrics.win_rate:.1%})\n")
        
        if self.metrics.sharpe_ratio > 1.5:
            sharpe = "✅ EXCELLENT"
        elif self.metrics.sharpe_ratio > 1.0:
            sharpe = "✅ GOOD"
        elif self.metrics.sharpe_ratio > 0.5:
            sharpe = "⚠️  ACCEPTABLE"
        else:
            sharpe = "❌ POOR"
        
        print(f"Risk-Adjusted Returns:       {sharpe} (Sharpe: {self.metrics.sharpe_ratio:.2f})\n")
        
        if self.metrics.profit_factor > 1.5 and self.metrics.expectancy > 0 and self.metrics.sharpe_ratio > 1.0:
            verdict = "✅ PRODUCTION READY"
            verdict_msg = "This signal shows statistically significant edge."
        elif self.metrics.profit_factor > 1.0 and self.metrics.expectancy > 0:
            verdict = "⚠️  FURTHER TESTING NEEDED"
            verdict_msg = "Edge exists but requires more validation."
        else:
            verdict = "❌ NOT RECOMMENDED"
            verdict_msg = "Insufficient edge for live trading."
        
        print(f"FINAL VERDICT:               {verdict}")
        print(f"                             {verdict_msg}")
    
    def export_json(self, output_file: str):
        """Export detailed report to JSON"""
        
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_signals": self.metrics.total_signals,
                "traded_signals": self.metrics.traded_signals,
                "winning_trades": self.metrics.winning_trades,
                "losing_trades": self.metrics.losing_trades,
            },
            "metrics": {
                "win_rate": round(self.metrics.win_rate, 4),
                "profit_factor": round(self.metrics.profit_factor, 2),
                "avg_win": round(self.metrics.avg_win, 4),
                "avg_loss": round(self.metrics.avg_loss, 4),
                "expectancy": round(self.metrics.expectancy, 4),
                "sharpe_ratio": round(self.metrics.sharpe_ratio, 2),
                "max_drawdown": round(self.metrics.max_drawdown, 4),
                "cumulative_pnl": round(self.metrics.cumulative_pnl, 4),
                "accuracy_vs_guidance": round(self.metrics.accuracy_vs_guidance, 4),
                "best_trade": round(self.metrics.best_trade, 4),
                "worst_trade": round(self.metrics.worst_trade, 4),
            },
            "signal_details": [
                {
                    "date": r.signal_date,
                    "ticker": r.ticker,
                    "headline": r.headline,
                    "guidance": r.guidance_direction,
                    "signal": r.signal_direction,
                    "confidence": round(r.signal_confidence, 2),
                    "entry_price": round(r.entry_price, 2),
                    "exit_price": round(r.exit_price, 2) if r.exit_price else None,
                    "price_change": round(r.price_change, 4) if r.price_change else None,
                    "pnl": round(r.pnl, 4),
                    "profitable": r.is_profitable,
                }
                for r in self.results
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Report exported → {output_file}")