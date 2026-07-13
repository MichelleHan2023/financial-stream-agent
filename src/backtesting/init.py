# src/backtesting/__init__.py
"""Backtesting module for signal validation"""

from .data_loader import RealDataLoader, RealHeadlineGenerator
from .signal_validator import SignalValidator
from .metrics_calculator import MetricsCalculator, BacktestMetrics
from .reporter import BacktestReporter
from .synthetic_data import generate_synthetic_prices

__all__ = [
    'RealDataLoader',
    'RealHeadlineGenerator',
    'SignalValidator',
    'MetricsCalculator',
    'BacktestMetrics',
    'BacktestReporter',
    'generate_synthetic_prices',
]