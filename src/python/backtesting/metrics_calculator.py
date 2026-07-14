# src/backtesting/metrics_calculator.py
import numpy as np
import logging
from typing import List
from dataclasses import dataclass
from .signal_validator import SignalResult

logger = logging.getLogger(__name__)

@dataclass
class BacktestMetrics:
    """Comprehensive backtesting metrics"""
    total_signals: int
    traded_signals: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    profit_factor: float
    avg_win: float
    avg_loss: float
    expectancy: float
    sharpe_ratio: float
    max_drawdown: float
    cumulative_pnl: float
    accuracy_vs_guidance: float
    best_trade: float
    worst_trade: float
    consecutive_wins: int
    consecutive_losses: int


class MetricsCalculator:
    """Calculate trading performance metrics from real backtests"""
    
    def __init__(self, signal_results: List[SignalResult]):
        self.results = signal_results
        self.logger = logging.getLogger(__name__)
    
    def calculate(self) -> BacktestMetrics:
        """Calculate all metrics"""
        
        if not self.results:
            raise ValueError("No signal results to analyze")
        
        traded = [r for r in self.results if r.signal_direction != "neutral"]
        
        if not traded:
            self.logger.warning("No trades executed")
            return None
        
        pnls = [r.pnl for r in traded]
        profitable = [r.pnl for r in traded if r.is_profitable]
        unprofitable = [r.pnl for r in traded if not r.is_profitable]
        
        win_rate = len(profitable) / len(traded) if traded else 0
        
        gross_profit = sum(profitable) if profitable else 0
        gross_loss = abs(sum(unprofitable)) if unprofitable else 0.0001
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        avg_win = np.mean(profitable) if profitable else 0
        avg_loss = np.mean(unprofitable) if unprofitable else 0
        
        expectancy = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)
        
        returns = np.array(pnls)
        mean_return = np.mean(returns)
        std_dev = np.std(returns)
        sharpe_ratio = (mean_return / std_dev * np.sqrt(252)) if std_dev > 0 else 0
        
        cumulative = np.cumsum(returns)
        peak = np.maximum.accumulate(cumulative)
        drawdown = (peak - cumulative) / np.abs(peak)
        max_drawdown = np.max(drawdown) if len(drawdown) > 0 else 0
        
        cumulative_pnl = sum(pnls)
        
        correct_guidance = sum(
            1 for r in traded
            if (r.guidance_direction == "raised" and r.price_change > 0) or
               (r.guidance_direction == "lowered" and r.price_change < 0)
        )
        accuracy_vs_guidance = correct_guidance / len(traded) if traded else 0
        
        best_trade = max(pnls) if pnls else 0
        worst_trade = min(pnls) if pnls else 0
        
        consecutive_wins = self._max_consecutive(pnls, lambda x: x > 0)
        consecutive_losses = self._max_consecutive(pnls, lambda x: x < 0)
        
        return BacktestMetrics(
            total_signals=len(self.results),
            traded_signals=len(traded),
            winning_trades=len(profitable),
            losing_trades=len(unprofitable),
            win_rate=win_rate,
            profit_factor=profit_factor,
            avg_win=avg_win,
            avg_loss=avg_loss,
            expectancy=expectancy,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            cumulative_pnl=cumulative_pnl,
            accuracy_vs_guidance=accuracy_vs_guidance,
            best_trade=best_trade,
            worst_trade=worst_trade,
            consecutive_wins=consecutive_wins,
            consecutive_losses=consecutive_losses,
        )
    
    @staticmethod
    def _max_consecutive(values, condition):
        """Calculate max consecutive values matching condition"""
        max_count = 0
        current_count = 0
        
        for val in values:
            if condition(val):
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 0
        
        return max_count