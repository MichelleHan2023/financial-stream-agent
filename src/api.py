from fastapi import FastAPI
from pydantic import BaseModel
from main import FinancialStreamAgent
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Financial Stream Agent", version="0.1.0")
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
    return {
        "headline": result["headline"],
        "sentiment": result["sentiment"],
        "signal": result["signal"],
        "trade_executed": result["trade_executed"]
    }

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