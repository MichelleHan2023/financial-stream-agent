import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict

from sentiment_analyzer import SentimentAnalyzer
from signal_extractor import SignalExtractor
from backtester import Backtester

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/trading_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FinancialStreamAgent:
    """Main agent that processes financial news and generates trading signals"""
    
    def __init__(self):
        """Initialize all components"""
        logger.info("Initializing Financial Stream Agent...")
        
        self.sentiment_analyzer = SentimentAnalyzer()
        self.signal_extractor = SignalExtractor()
        self.backtester = Backtester(initial_capital=10000)
        
        logger.info("Agent initialized successfully")
    
    def process_headline(self, headline: str, timestamp: datetime = None) -> Dict:
        """
        Process a single financial headline end-to-end
        
        Args:
            headline: Financial news headline
            timestamp: When the headline was published (default: now)
            
        Returns:
            {
                "headline": str,
                "sentiment": dict,
                "signal": dict,
                "trade_executed": bool,
                "trade_details": dict or None
            }
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        logger.info(f"Processing headline: {headline}")
        
        # Step 1: Analyze sentiment
        sentiment_result = self.sentiment_analyzer.analyze(headline)
        logger.info(f"Sentiment: {sentiment_result}")
        
        # Step 2: Extract signals
        signal = self.signal_extractor.extract_signals(
            headline, 
            sentiment_result["score"]
        )
        logger.info(f"Signal extracted: {signal}")
        
        # Step 3: Execute trading signal
        trade_result = self.backtester.execute_signal(signal, timestamp)
        trade_executed = trade_result["status"] == "executed"
        
        if trade_executed:
            logger.info(f"Trade executed: {trade_result['trade']}")
        else:
            logger.warning(f"Trade rejected: {trade_result['reason']}")
        
        result = {
            "headline": headline,
            "timestamp": timestamp.isoformat(),
            "sentiment": sentiment_result,
            "signal": signal,
            "trade_executed": trade_executed,
            "trade_details": trade_result["trade"] if trade_executed else None
        }
        
        return result
    
    def process_headlines_batch(self, headlines: List[str]) -> List[Dict]:
        """
        Process multiple headlines
        
        Args:
            headlines: List of financial headlines
            
        Returns:
            List of results for each headline
        """
        logger.info(f"Processing batch of {len(headlines)} headlines...")
        results = []
        
        for i, headline in enumerate(headlines, 1):
            result = self.process_headline(headline)
            results.append(result)
            logger.info(f"Processed {i}/{len(headlines)} headlines")
        
        return results
    
    def get_portfolio_summary(self) -> Dict:
        """Get current portfolio performance"""
        pnl = self.backtester.calculate_pnl()
        
        summary = {
            "portfolio_value": pnl["total_value"],
            "total_pnl": pnl["total_pnl"],
            "pnl_percent": pnl["pnl_percent"],
            "trades_executed": pnl["num_trades"],
            "current_positions": self.backtester.positions,
            "trade_history": self.backtester.get_trade_history()
        }
        
        logger.info(f"Portfolio Summary: {summary}")
        return summary
    
    def run_example(self):
        """Run example with sample headlines"""
        sample_headlines = [
            "Apple raises Q4 guidance as iPhone 15 demand exceeds expectations",
            "Tesla cuts 2024 profit forecast amid competition and EV slowdown",
            "Microsoft maintains cloud growth momentum with strong Azure performance",
            "Meta beats earnings estimates with AI infrastructure investments paying off",
            "Amazon disappointed investors with lower-than-expected AWS margins"
        ]
        
        logger.info("="*60)
        logger.info("FINANCIAL STREAM AGENT - EXAMPLE RUN")
        logger.info("="*60)
        
        # Process headlines
        results = self.process_headlines_batch(sample_headlines)
        
        # Print results
        for result in results:
            print("\n" + "-"*60)
            print(f"Headline: {result['headline']}")
            print(f"Sentiment: {result['sentiment']['sentiment']} ({result['sentiment']['score']})")
            print(f"Ticker: {result['signal']['ticker']}")
            print(f"Guidance: {result['signal']['guidance_direction']}")
            print(f"Trade Executed: {result['trade_executed']}")
            if result['trade_executed']:
                trade = result['trade_details']
                print(f"  → {trade['action']} {trade['quantity']} x {trade['ticker']} @ ${trade['price']:.2f}")
        
        # Print portfolio summary
        print("\n" + "="*60)
        print("PORTFOLIO SUMMARY")
        print("="*60)
        summary = self.get_portfolio_summary()
        print(f"Portfolio Value: ${summary['portfolio_value']:.2f}")
        print(f"Total P&L: ${summary['total_pnl']:.2f} ({summary['pnl_percent']:.2f}%)")
        print(f"Trades Executed: {summary['trades_executed']}")
        print(f"Current Positions: {summary['current_positions']}")

def main():
    """Main entry point"""
    try:
        agent = FinancialStreamAgent()
        agent.run_example()
    except Exception as e:
        logger.error(f"Error running agent: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()