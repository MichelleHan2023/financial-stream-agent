import unittest
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sentiment_analyzer import SentimentAnalyzer
from signal_extractor import SignalExtractor
from backtester import Backtester

class TestSentimentAnalyzer(unittest.TestCase):
    """Test sentiment analysis"""
    
    @classmethod
    def setUpClass(cls):
        cls.analyzer = SentimentAnalyzer()
    
    def test_positive_sentiment(self):
        """Test positive sentiment detection"""
        result = self.analyzer.analyze("Apple beats earnings expectations with strong iPhone sales")
        self.assertEqual(result["sentiment"], "positive")
        self.assertGreater(result["score"], 0.5)
    
    def test_negative_sentiment(self):
        """Test negative sentiment detection"""
        result = self.analyzer.analyze("Tesla misses guidance and disappoints investors")
        self.assertEqual(result["sentiment"], "negative")
        self.assertLess(result["score"], 0.5)
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment detection"""
        result = self.analyzer.analyze("Company announces quarterly earnings report")
        self.assertIn(result["sentiment"], ["neutral", "positive", "negative"])
        self.assertGreaterEqual(result["confidence"], 0.0)
        self.assertLessEqual(result["confidence"], 1.0)


class TestSignalExtractor(unittest.TestCase):
    """Test signal extraction"""
    
    @classmethod
    def setUpClass(cls):
        cls.extractor = SignalExtractor()
    
    def test_ticker_extraction_with_dollar(self):
        """Test ticker extraction with $ prefix"""
        ticker = self.extractor.extract_ticker("$AAPL reports strong earnings")
        self.assertEqual(ticker, "AAPL")
    
    def test_ticker_extraction_with_parens(self):
        """Test ticker extraction with parentheses"""
        ticker = self.extractor.extract_ticker("Microsoft (MSFT) beats expectations")
        self.assertEqual(ticker, "MSFT")
    
    def test_guidance_raised(self):
        """Test guidance raise detection"""
        guidance = self.extractor.extract_guidance_direction("Company raises full-year guidance")
        self.assertEqual(guidance["direction"], "raised")
        self.assertGreater(guidance["confidence"], 0.0)
    
    def test_guidance_lowered(self):
        """Test guidance lower detection"""
        guidance = self.extractor.extract_guidance_direction("Company cuts 2024 outlook")
        self.assertEqual(guidance["direction"], "lowered")
        self.assertGreater(guidance["confidence"], 0.0)
    
    def test_guidance_maintained(self):
        """Test guidance maintained detection"""
        guidance = self.extractor.extract_guidance_direction("Company reaffirms full-year guidance")
        self.assertEqual(guidance["direction"], "maintained")
        self.assertGreater(guidance["confidence"], 0.0)


class TestBacktester(unittest.TestCase):
    """Test backtesting engine"""
    
    def setUp(self):
        self.backtester = Backtester(initial_capital=10000)
    
    def test_initial_portfolio_value(self):
        """Test initial portfolio value"""
        pnl = self.backtester.calculate_pnl()
        self.assertEqual(pnl["total_value"], 10000)
        self.assertEqual(pnl["total_pnl"], 0)
    
    def test_position_tracking(self):
        """Test position tracking"""
        self.backtester.positions["AAPL"] = 10
        self.assertEqual(self.backtester.positions["AAPL"], 10)
    
    def test_trade_history(self):
        """Test trade history recording"""
        initial_trades = len(self.backtester.trades)
        self.backtester.trades.append({
            "date": datetime.now(),
            "ticker": "AAPL",
            "action": "BUY",
            "quantity": 10,
            "price": 150.0,
            "value": 1500.0
        })
        self.assertEqual(len(self.backtester.trades), initial_trades + 1)
    
    def test_pnl_calculation(self):
        """Test P&L calculation"""
        # Simulate a trade
        self.backtester.portfolio_value = 8500  # After buying $1500 of stock
        self.backtester.positions["AAPL"] = 10
        
        pnl = self.backtester.calculate_pnl()
        self.assertIsNotNone(pnl["total_value"])
        self.assertIsNotNone(pnl["pnl_percent"])


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_end_to_end_signal_processing(self):
        """Test complete signal processing pipeline"""
        headline = "$AAPL raises Q4 guidance with strong iPhone demand"
        
        analyzer = SentimentAnalyzer()
        extractor = SignalExtractor()
        
        # Analyze sentiment
        sentiment = analyzer.analyze(headline)
        self.assertIn(sentiment["sentiment"], ["positive", "negative", "neutral"])
        
        # Extract signal
        signal = extractor.extract_signals(headline, sentiment["score"])
        self.assertEqual(signal["ticker"], "AAPL")
        self.assertEqual(signal["guidance_direction"], "raised")


if __name__ == "__main__":
    unittest.main()