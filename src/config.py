"""
Configuration settings for Financial Stream Agent
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys and Credentials
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "")

# Model Settings
FINBERT_MODEL = "ProsusAI/finbert"
SPACY_MODEL = "en_core_web_sm"

# Trading Settings
INITIAL_CAPITAL = 10000
POSITION_SIZE = 0.1  # 10% of portfolio per trade
MAX_POSITIONS = 5

# Backtesting Settings
BACKTEST_PERIOD = "1y"
BACKTEST_START_DATE = None  # None = use BACKTEST_PERIOD

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "../logs/trading_agent.log"

# Data Settings
DATA_DIR = "../data"
CACHE_ENABLED = True
CACHE_TTL = 3600  # seconds