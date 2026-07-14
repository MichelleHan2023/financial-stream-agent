#include "../include/trading_engine.h"
#include <cmath>
#include <chrono>
#include <iomanip>
#include <sstream>

TradingEngine::TradingEngine() 
    : metrics{0, 0, 0.0, 0.0, 0.0, 0.0} {}

TradingEngine::~TradingEngine() {}

double TradingEngine::calculate_position_size(double account_balance, double risk_percent) {
    // Risk Management: Position sizing based on account risk
    return account_balance * (risk_percent / 100.0);
}

bool TradingEngine::validate_signal(const Signal& signal) {
    // Validate signal before processing
    if (signal.ticker.empty()) {
        std::cerr << "ERROR: Empty ticker" << std::endl;
        return false;
    }
    
    if (signal.confidence < 0.0 || signal.confidence > 1.0) {
        std::cerr << "ERROR: Invalid confidence score" << std::endl;
        return false;
    }
    
    if (signal.recommendation != "BUY" && 
        signal.recommendation != "SELL" && 
        signal.recommendation != "HOLD") {
        std::cerr << "ERROR: Invalid recommendation" << std::endl;
        return false;
    }
    
    return true;
}

bool TradingEngine::process_signal(const Signal& signal, double account_balance) {
    std::cout << "\n=== Processing Signal ===" << std::endl;
    std::cout << "Ticker: " << signal.ticker << std::endl;
    std::cout << "Recommendation: " << signal.recommendation << std::endl;
    std::cout << "Confidence: " << signal.confidence << std::endl;
    std::cout << "Sentiment: " << signal.sentiment_score << std::endl;
    
    // Validate signal
    if (!validate_signal(signal)) {
        return false;
    }
    
    // Store processed signal
    processed_signals.push_back(signal);
    
    // Execute trade if confidence threshold met
    if (signal.confidence > 0.65) {
        Position position;
        position.ticker = signal.ticker;
        position.direction = (signal.recommendation == "BUY") ? "LONG" : "SHORT";
        position.entry_price = 100.0;  // Placeholder - would come from market data
        position.position_size = calculate_position_size(account_balance, 2.0);  // 2% risk
        position.stop_loss = position.entry_price * 0.98;  // 2% stop loss
        position.take_profit = position.entry_price * 1.05;  // 5% take profit
        
        open_positions.push_back(position);
        
        std::cout << "✅ Position opened: " << position.direction 
                  << " " << position.ticker 
                  << " | Size: $" << position.position_size << std::endl;
        
        metrics.total_trades++;
        return true;
    } else {
        std::cout << "⏸️  Signal confidence below threshold (0.65)" << std::endl;
        return false;
    }
}

void TradingEngine::stream_market_data(const std::string& json_data) {
    // Process incoming market data stream
    std::cout << "\n=== Market Data Stream ===" << std::endl;
    std::cout << "Processing: " << json_data << std::endl;
    
    // Check stop loss and take profit levels
    check_stop_loss_take_profit();
}

void TradingEngine::apply_risk_management(Position& position) {
    // Apply risk management rules
    std::cout << "Applying risk management to " << position.ticker << std::endl;
    
    // Trailing stop loss (adjusts up but not down)
    // Position sizing already applied
    // Volatility-based adjustments would go here
}

void TradingEngine::check_stop_loss_take_profit() {
    // Simulate checking SL/TP levels
    for (auto& pos : open_positions) {
        // In real implementation, compare against live market price
        std::cout << "Checking SL/TP for " << pos.ticker 
                  << " | SL: $" << pos.stop_loss 
                  << " | TP: $" << pos.take_profit << std::endl;
    }
}

PerformanceMetrics TradingEngine::get_metrics() const {
    return metrics;
}

void TradingEngine::log_trade(const Position& position, const std::string& status) {
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    
    std::cout << "[" << std::put_time(std::localtime(&time), "%Y-%m-%d %H:%M:%S") << "] "
              << "Trade: " << position.ticker 
              << " | Direction: " << position.direction 
              << " | Status: " << status << std::endl;
}

std::string TradingEngine::signal_to_json(const Signal& signal) const {
    std::stringstream ss;
    ss << "{"
       << "\"ticker\": \"" << signal.ticker << "\", "
       << "\"recommendation\": \"" << signal.recommendation << "\", "
       << "\"confidence\": " << signal.confidence << ", "
       << "\"sentiment_score\": " << signal.sentiment_score
       << "}";
    return ss.str();
}

std::vector<Position> TradingEngine::get_open_positions() const {
    return open_positions;
}

// Main entry point
int main() {
    std::cout << "=== C++ Trading Engine ===" << std::endl;
    std::cout << "High-Performance Stream Processing for Financial Signals" << std::endl;
    
    TradingEngine engine;
    double account_balance = 100000.0;
    
    // Simulate signals from Python API
    Signal test_signal1{
        "AAPL",
        "BUY",
        0.85,
        0.92,
        "2026-07-14 23:30:00"
    };
    
    Signal test_signal2{
        "TSLA",
        "SELL",
        0.78,
        -0.88,
        "2026-07-14 23:31:00"
    };
    
    // Process signals
    engine.process_signal(test_signal1, account_balance);
    engine.process_signal(test_signal2, account_balance);
    
    // Stream market data
    engine.stream_market_data("{\"AAPL\": 150.25, \"TSLA\": 245.50}");
    
    // Display metrics
    auto metrics = engine.get_metrics();
    std::cout << "\n=== Performance Metrics ===" << std::endl;
    std::cout << "Total Trades: " << metrics.total_trades << std::endl;
    std::cout << "Winning Trades: " << metrics.winning_trades << std::endl;
    
    // Display open positions
    std::cout << "\n=== Open Positions ===" << std::endl;
    for (const auto& pos : engine.get_open_positions()) {
        std::cout << pos.ticker << " | " << pos.direction 
                  << " | Size: $" << pos.position_size << std::endl;
    }
    
    return 0;
}
