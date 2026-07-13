from fastapi import FastAPI
from pydantic import BaseModel
from news_fetcher import NewsFetcher
from sentiment_analyzer import SentimentAnalyzer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Financial Stream Agent", version="0.1.0")

# Initialize components
sentiment_analyzer = SentimentAnalyzer()

class FinancialStreamAgent:
    """Main agent orchestrator"""
    def __init__(self):
        self.sentiment_analyzer = sentiment_analyzer
        self.portfolio = {}
        self.trades = []
    
    def process_headline(self, headline: str):
        """Process single headline and return signal"""
        try:
            # Get sentiment from FinBERT
            sentiment_result = self.sentiment_analyzer.analyze(headline)
            
            # sentiment_result has keys: sentiment, score, confidence
            sentiment_label = sentiment_result.get("sentiment", "neutral").upper()
            confidence = sentiment_result.get("confidence", 0)
            
            # Map to trading signal
            if sentiment_label == "POSITIVE":
                recommendation = "BUY"
            elif sentiment_label == "NEGATIVE":
                recommendation = "SELL"
            else:
                recommendation = "HOLD"
            
            signal = {
                "recommendation": recommendation,
                "confidence": confidence,
                "headline": headline,
                "label": sentiment_label
            }
            
            # Track trade
            trade_executed = recommendation != "HOLD"
            if trade_executed:
                self.trades.append({
                    "headline": headline,
                    "signal": signal,
                    "sentiment": sentiment_result,
                    "timestamp": str(datetime.now())
                })
            
            # Return with correct structure for API response
            return {
                "headline": headline,
                "sentiment": {
                    "label": sentiment_label,
                    "score": sentiment_result.get("score", 0.5),
                    "confidence": confidence
                },
                "signal": signal,
                "trade_executed": trade_executed
            }
        except Exception as e:
            logger.error(f"Error processing headline: {e}")
            import traceback
            traceback.print_exc()
            return {
                "headline": headline,
                "sentiment": {"label": "ERROR", "score": 0, "confidence": 0},
                "signal": {"recommendation": "HOLD"},
                "trade_executed": False
            }
    
    def get_portfolio_summary(self):
        """Get portfolio stats"""
        return {
            "total_trades": len(self.trades),
            "trades": self.trades[-10:] if self.trades else [],
            "buy_signals": sum(1 for t in self.trades if t["signal"]["recommendation"] == "BUY"),
            "sell_signals": sum(1 for t in self.trades if t["signal"]["recommendation"] == "SELL")
        }

# Initialize agent
agent = FinancialStreamAgent()

class HeadlineRequest(BaseModel):
    headline: str

class HeadlineResponse(BaseModel):
    headline: str
    sentiment: dict
    signal: dict
    trade_executed: bool

@app.post("/analyze", response_model=HeadlineResponse)
def analyze_headline(request: HeadlineRequest):
    """Analyze a financial headline and generate trading signal"""
    result = agent.process_headline(request.headline)
    return result

@app.get("/portfolio")
def get_portfolio_summary():
    """Get current portfolio summary"""
    return agent.get_portfolio_summary()

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)