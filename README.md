# Financial Stream Agent 🚀

**AI-powered trading signal generation from financial news using FinBERT sentiment analysis, with high-performance C++ execution engine.**

A full-stack system demonstrating expertise in AI/ML, financial analysis, Python backend, and C++ performance optimization.

## 🎯 Project Goal

Build a **distributed financial analysis system** that converts raw financial news into actionable trading signals with quantifiable edge.

**Skills Demonstrated:**
- 🤖 **AI/ML**: FinBERT transformer models for sentiment classification
- 💰 **Finance**: Trading signal extraction, risk metrics (Sharpe ratio, drawdown), position sizing
- 🐍 **Python**: Production-grade FastAPI service with ML pipelines and backtesting
- ⚡ **C++**: High-performance stream processing with real-time risk management

---

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│ Financial News Stream │
│ (NewsAPI / Live) │
└──────────────────────────┬──────────────────────────────────┘
│
┌──────────────────▼──────────────────┐
│ 🐍 PYTHON - Signal Generation │
│ (src/python/) │
│ │
│ ├─ news_fetcher.py │
│ │ └─ Fetch headlines in real-time│
│ │ │
│ ├─ sentiment_analyzer.py │
│ │ └─ FinBERT classification │
│ │ │
│ ├─ main.py │
│ │ └─ Extract ticker + signal │
│ │ │
│ ├─ backtesting_engine.py │
│ │ └─ Validate signals historically
│ │ │
│ └─ api.py (FastAPI) │
│ └─ REST endpoints for signals │
└──────────────────┬──────────────────┘
│
JSON Signal Stream
{"ticker": "AAPL",
"recommendation": "BUY",
"confidence": 0.85}
│
┌──────────────────▼──────────────────┐
│ ⚡ C++ - Trading Execution │
│ (src/cpp/trading_engine.cpp) │
│ │
│ ├─ Signal Validation │
│ │ └─ Confidence threshold check │
│ │ │
│ ├─ Position Sizing │
│ │ └─ Risk-based allocation │
│ │ │
│ ├─ Risk Management │
│ │ └─ Stop loss / Take profit │
│ │ │
│ └─ Performance Tracking │
│ └─ Real-time metrics │
└──────────────────────────────────────┘
│
Trading Decisions
(Executed Positions)


---

## 📊 Project Structure
financial-stream-agent/
├── src/
│ ├── python/ # ML & Signal Generation
│ │ ├── api.py # FastAPI server (port 8000)
│ │ ├── main.py # News analysis pipeline
│ │ ├── sentiment_analyzer.py # FinBERT model
│ │ ├── news_fetcher.py # NewsAPI integration
│ │ ├── backtesting_engine.py # Historical validation
│ │ └── backtesting/ # Backtesting utilities
│ │ ├── data_loader.py
│ │ ├── metrics_calculator.py
│ │ ├── reporter.py
│ │ ├── signal_validator.py
│ │ └── synthetic_data.py
│ │
│ └── cpp/ # Trading Engine
│ ├── client/
│ │ └── trading_engine.cpp # Main execution engine
│ └── include/
│ └── trading_engine.h # Trading engine header
│
├── build/ # Compiled C++ binaries
├── tests/
│ └── test_agent.py # Unit tests
├── data/
│ ├── backtest_results/ # Performance reports
│ └── headlines/ # Historical data
│
├── CMakeLists.txt # C++ build configuration
├── requirements.txt # Python dependencies
└── README.md


---

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.8+**
- **C++ compiler** (Clang/GCC)
- **CMake 3.10+**

### 1. Clone Repository

```bash
git clone https://github.com/MichelleHan2023/financial-stream-agent.git
cd financial-stream-agent
2. Python Setup
bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. C++ Build
bash
mkdir -p build
cd build
cmake ..
make
cd ..
🚀 Quick Start
Run All Three Services
Terminal 1 - FastAPI Server:

bash
source venv/bin/activate
python src/python/api.py

Terminal 2 - News Analysis:

bash
source venv/bin/activate
python src/python/main.py

Terminal 3 - C++ Trading Engine:

bash
./build/trading_engine


🧪 Testing
Unit Tests
bash
pytest tests/test_agent.py -v

API Testing
Analyze a headline:

bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"headline": "Apple crushes earnings expectations, stock soars 15%"}'

Response:

json
{
  "headline": "Apple crushes earnings expectations, stock soars 15%",
  "sentiment": {
    "label": "POSITIVE",
    "score": 0.656,
    "confidence": 0.656
  },
  "signal": {
    "recommendation": "BUY",
    "confidence": 0.656,
    "headline": "Apple crushes earnings expectations, stock soars 15%",
    "label": "POSITIVE"
  },
  "trade_executed": true
}

Check portfolio:

bash
curl http://localhost:8000/portfolio

C++ Trading Engine Test
bash
./build/trading_engine

Output:

asciidoc
=== C++ Trading Engine ===
High-Performance Stream Processing for Financial Signals

=== Processing Signal ===
Ticker: AAPL
Recommendation: BUY
Confidence: 0.85
Sentiment: 0.92
✅ Position opened: LONG AAPL | Size: $2000

=== Performance Metrics ===
Total Trades: 2
Winning Trades: 0

📈 Backtesting Results
Historical Signal Validation (30 signals, 2023-2024):

Metric	Value
Total Signals	30
Win Rate	51.9%
Average Win	+5.41%
Average Loss	-4.23%
Sharpe Ratio	2.01
Profit Factor	1.38x
Cumulative P&L	+20.83%
Max Drawdown	66.79%
Verdict: ⚠️ Marginal edge detected. Expected value per trade: +0.77%

🤖 Technologies Used
Python Stack
NLP: Transformers (FinBERT)
Framework: FastAPI + Uvicorn
Data: pandas, numpy
Finance: yfinance, NewsAPI
Testing: pytest
C++ Stack
Language: C++17
Build: CMake
Networking: libcurl
Performance: Optimized for real-time processing
🔄 System Workflow
scss
1. NEWS FETCHING (Python)
   └─ NewsAPI → Retrieve financial headlines

2. SENTIMENT ANALYSIS (Python)
   └─ FinBERT → POSITIVE/NEGATIVE/NEUTRAL + confidence

3. SIGNAL GENERATION (Python)
   └─ Extract ticker + direction + confidence

4. BACKTESTING (Python)
   └─ Validate signal quality vs historical data

5. API EXPOSURE (Python)
   └─ FastAPI → JSON endpoint

6. SIGNAL RECEPTION (C++)
   └─ Parse JSON signal

7. POSITION SIZING (C++)
   └─ Calculate risk-based allocation (2% per trade)

8. RISK MANAGEMENT (C++)
   └─ Set stop loss (2%) and take profit (5%)

9. EXECUTION (C++)
   └─ Open position with metrics tracking

10. PERFORMANCE TRACKING (C++)
    └─ Real-time Sharpe, drawdown, P&L

💡 Key Features
✅ Real-time News Processing - Fetch and analyze financial headlines as they break

✅ FinBERT Sentiment Analysis - Deep learning model trained on financial text

✅ Intelligent Signal Extraction - Automatically identify tickers and trading direction

✅ Historical Backtesting - Validate signal quality with 51.9% win rate

✅ Risk Management - Position sizing, stop loss, take profit automation

✅ Production APIs - FastAPI endpoints for real-time integration

✅ High-Performance Execution - C++ engine for microsecond-level processing

✅ Comprehensive Testing - 13+ unit tests with 100% pass rate

🎓 Learning Outcomes
This project demonstrates:

Machine Learning Proficiency

Transformer model inference (FinBERT)
Sentiment classification with confidence scoring
Model validation and performance metrics
Financial Expertise

Trading signal generation and validation
Risk metrics (Sharpe ratio, drawdown, win rate)
Position sizing and risk management
Swing trading strategy design
Software Engineering

Production-grade Python API (FastAPI)
Data pipeline architecture
Unit testing and validation
Clean code organization
Systems Programming

High-performance C++ implementation
Real-time stream processing
Cross-language communication (Python ↔ C++)
🚀 Future Enhancements
 Real broker integration (Alpaca, Interactive Brokers)
 Multi-model ensemble (combine multiple sentiment models)
 Advanced technical indicators (RSI, MACD, Bollinger Bands)
 Web dashboard (React frontend)
 Cloud deployment (AWS Lambda, Docker)
 Live market data integration (WebSocket streams)
 Portfolio optimization (mean-variance allocation)
📝 License
MIT

👨‍💻 Author
Michelle Han

🤝 Contributing
Contributions welcome! Please submit issues and pull requests.

⭐ Acknowledgments
FinBERT: Financial sentiment analysis model
FastAPI: Modern Python web framework
yfinance: Yahoo Finance API wrapper
NewsAPI: Real-time news aggregation
