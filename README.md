# Financial Stream Agent 🚀

AI-powered trading signal generation from financial news headlines using FinBERT sentiment analysis and intelligent backtesting.

## Features

- **Sentiment Analysis**: FinBERT-based classification (positive/negative/neutral)
- **Signal Extraction**: Automatic ticker detection and BUY/SELL/HOLD recommendations
- **Backtesting Engine**: Historical P&L validation (51.9% win rate, Sharpe 2.01)
- **REST API**: FastAPI endpoints for real-time analysis
- **News Integration**: Real-time NewsAPI integration
- **Comprehensive Testing**: 13+ unit tests with 100% pass rate

## Quick Start

### Installation

```bash
git clone https://github.com/MichelleHan2023/financial-stream-agent.git
cd financial-stream-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txtRun the System
Terminal 1 - API Server:

bash
python src/api.py

Terminal 2 - News Analysis:

bash
python src/main.py

Terminal 3 - Backtesting:

bash
python src/backtesting_engine.py


API Usage
Analyze a Headline
bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"headline": "Apple crushes earnings expectations, stock soars 15%"}'

Response:

json
{
  "headline": "Apple crushes earnings expectations, stock soars 15%",
  "sentiment": {"label": "POSITIVE", "score": 0.656},
  "signal": {"recommendation": "BUY", "confidence": 0.656},
  "trade_executed": true
}

Check Portfolio
bash
curl http://localhost:8000/portfolio

Backtesting Results
Total Signals: 30
Win Rate: 51.9%
Average Win: +5.41%
Average Loss: -4.23%
Sharpe Ratio: 2.01
Cumulative P&L: +20.83%
Profit Factor: 1.38x
Project Structure
mipsasm
financial-stream-agent/
├── src/
│   ├── api.py                 # FastAPI server
│   ├── main.py                # News analysis pipeline
│   ├── backtesting_engine.py  # Historical validation
│   ├── sentiment_analyzer.py  # FinBERT model
│   ├── news_fetcher.py        # NewsAPI integration
│   └── backtesting/           # Backtesting utilities
├── tests/
│   └── test_agent.py          # Unit tests
├── data/
│   ├── backtest_results/      # Reports & metrics
│   └── headlines/             # Historical data
├── requirements.txt           # Python dependencies
└── README.md

Requirements
Python 3.8+
PyTorch (transformers)
FastAPI & Uvicorn
pandas, numpy
yfinance, newsapi-python
Testing
bash
pytest tests/test_agent.py -v

Technologies
NLP: FinBERT (Transformers)
API: FastAPI
Data: yfinance, NewsAPI
Testing: pytest
Future Enhancements
 Real broker integration (Alpaca/Interactive Brokers)
 Multi-model ensemble
 Web dashboard
 Cloud deployment
 Advanced technical indicators
License
MIT

Author
Michelle Han
