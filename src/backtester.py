#!/usr/bin/env python3
"""
Phase 3: Real-World Backtesting Engine
Validates signal quality against historical data
"""

import logging
import os
from datetime import datetime
from backtesting.data_loader import RealDataLoader, RealHeadlineGenerator
from backtesting.signal_validator import SignalValidator
from backtesting.metrics_calculator import MetricsCalculator
from backtesting.reporter import BacktestReporter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_backtest(
    start_date: str = "2023-01-01",
    end_date: str = "2024-12-31",
    holding_period: int = 5,
    headlines_file: str = "data/headlines/historical_headlines.json"
):
    """Run complete backtesting pipeline with real data"""
    
    print("\n" + "="*100)
    print("🚀 PHASE 3: REAL-WORLD BACKTESTING ENGINE")
    print("   Validating signals against historical price data from yfinance")
    print("="*100 + "\n")
    
    os.makedirs("data/headlines", exist_ok=True)
    os.makedirs("data/backtest_results", exist_ok=True)
    
    print("📝 Step 1: Preparing historical headlines...")
    headlines = RealHeadlineGenerator.generate_realistic(headlines_file)
    
    print("\n📊 Step 2: Loading real historical price data from yfinance...\n")
    data_loader = RealDataLoader(start_date, end_date)
    
    tickers = list(set(h['ticker'] for h in headlines))
    data_loader.fetch_price_data(tickers)
    
    print("\n🔬 Step 3: Validating signals against real price data...\n")
    validator = SignalValidator(data_loader, holding_period=holding_period)
    results = validator.validate_signals(headlines)
    
    if not results:
        print("❌ No valid signals to analyze")
        return None
    
    print("\n📈 Step 4: Calculating performance metrics...\n")
    calculator = MetricsCalculator(results)
    metrics = calculator.calculate()
    
    if not metrics:
        print("❌ Could not calculate metrics")
        return None
    
    print("\n📄 Step 5: Generating backtest report...\n")
    reporter = BacktestReporter(results, metrics)
    reporter.print_summary()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"data/backtest_results/backtest_report_{timestamp}.json"
    reporter.export_json(report_file)
    
    print(f"\n✅ Backtesting complete!")
    print(f"   Tested: {metrics.total_signals} signals")
    print(f"   Traded: {metrics.traded_signals} signals")
    print(f"   Win Rate: {metrics.win_rate:.1%}")
    print(f"   Sharpe: {metrics.sharpe_ratio:.2f}")
    print(f"   Report: {report_file}\n")
    
    return metrics, results

if __name__ == "__main__":
    metrics, results = run_backtest(
        start_date="2023-01-01",
        end_date="2024-12-31",
        holding_period=5
    )