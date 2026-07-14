#ifndef TRADING_ENGINE_H
#define TRADING_ENGINE_H

#include <string>
#include <vector>
#include <map>
#include <iostream>

struct Signal {
    std::string ticker;
    std::string recommendation;  // BUY, SELL, HOLD
    double confidence;
    double sentiment_score;
    std::string timestamp;
};

struct Position {
    std::string ticker;
    std::string direction;  // LONG, SHORT
    double entry_price;
    double position_size;
    double stop_loss;
    double take_profit;
};

struct PerformanceMetrics {
    int total_trades;
    int winning_trades;
    double win_rate;
    double sharpe_ratio;
    double max_drawdown;
    double cumulative_pnl;
};

class TradingEngine {
private:
    std::vector<Position> open_positions;
    std::vector<Signal> processed_signals;
    PerformanceMetrics metrics;
    
    double calculate_position_size(double account_balance, double risk_percent);
    bool validate_signal(const Signal& signal);
    void update_metrics();

public:
    TradingEngine();
    ~TradingEngine();
    
    // Process incoming signal from Python API
    bool process_signal(const Signal& signal, double account_balance);
    
    // Stream processing
    void stream_market_data(const std::string& json_data);
    
    // Risk management
    void apply_risk_management(Position& position);
    void check_stop_loss_take_profit();
    
    // Performance tracking
    PerformanceMetrics get_metrics() const;
    void log_trade(const Position& position, const std::string& status);
    
    // Utilities
    std::string signal_to_json(const Signal& signal) const;
    std::vector<Position> get_open_positions() const;
};

#endif // TRADING_ENGINE_H
