import logging
import os
from news_fetcher import NewsFetcher
from sentiment_analyzer import SentimentAnalyzer
from dotenv import load_dotenv
import re

load_dotenv()

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/trading_agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Common stock tickers
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'AMD', 'LCID', 'RXT']

def extract_ticker(text):
    """Extract stock ticker from text"""
    for ticker in TICKERS:
        if ticker in text.upper():
            return ticker
    return "N/A"

def get_signal(sentiment):
    """Convert sentiment to trading signal"""
    if 'positive' in sentiment.lower():
        return "BUY"
    elif 'negative' in sentiment.lower():
        return "SELL"
    else:
        return "NEUTRAL"

def main():
    """Main entry point"""
    try:
        logger.info("Starting Financial Stream Agent...")
        
        # Fetch real news
        logger.info("Fetching financial news from NewsAPI...")
        news_fetcher = NewsFetcher()
        articles = news_fetcher.fetch_financial_news("earnings announcement", limit=10)
        
        if not articles:
            logger.warning("No articles found.")
            return
        
        # Initialize AI model
        logger.info("Loading AI models...")
        sentiment_analyzer = SentimentAnalyzer()
        
        # Process each article
        logger.info(f"Processing {len(articles)} articles...")
        print("\n" + "="*80)
        print("FINANCIAL STREAM AGENT - TRADING SIGNALS")
        print("="*80 + "\n")
        
        for i, article in enumerate(articles, 1):
            headline = article.get('title', '')
            
            if not headline:
                continue
            
            print(f"Article {i}: {headline}")
            print(f"Source: {article.get('source', 'Unknown')}")
            
            # Analyze sentiment
            try:
                sentiment_result = sentiment_analyzer.analyze(headline)
                
                # Handle different response formats
                if isinstance(sentiment_result, list) and len(sentiment_result) > 0:
                    sentiment_dict = sentiment_result[0]
                    sentiment_label = sentiment_dict.get('label', 'neutral')
                    sentiment_score = sentiment_dict.get('score', 0.0)
                elif isinstance(sentiment_result, dict):
                    sentiment_label = sentiment_result.get('label', 'neutral')
                    sentiment_score = sentiment_result.get('score', 0.0)
                else:
                    sentiment_label = 'neutral'
                    sentiment_score = 0.0
                
                print(f"Sentiment: {sentiment_label.upper()} (confidence: {sentiment_score:.2f})")
                
                # Extract ticker and generate signal
                ticker = extract_ticker(headline)
                signal = get_signal(sentiment_label)
                
                print(f"Ticker: {ticker}")
                print(f"Signal: {signal}")
                print(f"Recommendation: {'BUY' if signal == 'BUY' else 'SELL' if signal == 'SELL' else 'HOLD'} {ticker if ticker != 'N/A' else ''}")
                
            except Exception as e:
                print(f"Error processing article: {e}")
            
            print("-" * 80 + "\n")
        
        logger.info("Analysis complete!")
        
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)

if __name__ == "__main__":
    main()
