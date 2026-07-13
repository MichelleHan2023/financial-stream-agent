# Financial Stream Agent 🚀

AI-powered trading signal generation from financial news headlines using FinBERT sentiment analysis and intelligent signal extraction.

## Features

- **Sentiment Analysis**: FinBERT-based sentiment classification (positive/negative/neutral)
- **Signal Extraction**: Automatic ticker and guidance direction detection
- **Backtesting Engine**: Historical P&L simulation
- **REST API**: FastAPI endpoints for real-time analysis
- **Comprehensive Testing**: 13+ unit tests with 100% pass rate

## Quick Start

### Installation

```bash
# Clone and setup
git clone <repo>
cd financial-stream-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt