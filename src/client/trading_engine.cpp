#include <iostream>
#include <curl/curl.h>
#include <json/json.h>
#include <vector>
#include <chrono>
#include <cmath>
#include <sstream>

struct Position {
    std::string ticker;
    int quantity;
    double entry_price;
    double current_price;
};

struct PerformanceMetrics {
    double sharpe_ratio;
    double max_drawdown;
    double total_pnl;
};

class TradingEngine {
private:
    std::string python_api_url;
    std::vector<Position> positions;
    double cash_balance;
    double initial_capital;
    std::vector<double> equity_curve;
    
public:
    TradingEngine(std::string api_url, double initial_balance) 
        : python_api_url(api_url), cash_balance(initial_balance), initial_capital(initial_balance) {}
    
    static size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* userp) {
        userp->append((char*)contents, size * nmemb);
        return size * nmemb;
    }
    
    Json::Value analyzeHeadline(const std::string& headline) {
        CURL* curl = curl_easy_init();
        std::string readBuffer;
        
        Json::Value root;
        root["headline"] = headline;
        
        Json::StreamWriterBuilder writer;
        std::string json_data = Json::writeString(writer, root);
        
        if (curl) {
            curl_easy_setopt(curl, CURLOPT_URL, (python_api_url + "/analyze").c_str());
            curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_data.c_str());
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
            
            struct curl_slist* headers = NULL;
            headers = curl_slist_append(headers, "Content-Type: application/json");
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
            
            CURLcode res = curl_easy_perform(curl);
            
            if (res != CURLE_OK) {
                std::cerr << "CURL error: " << curl_easy_strerror(res) << std::endl;
                return Json::Value();
            }
            
            curl_slist_free_all(headers);
            curl_easy_cleanup(curl);
        }
        
        Json::Value response;
        Json::CharReaderBuilder reader;
        std::string errs;
        std::istringstream s(readBuffer);
        
        if (!Json::parseFromStream(reader, s, &response, &errs)) {
            std::cerr << "JSON parse error: " << errs << std::endl;
            return Json::Value();
        }
        
        return response;
    }
    
    void executeTrade(const Json::Value& signal) {
        if (signal.empty() || !signal.isMember("signal")) return;
        
        std::string ticker = signal["signal"]["ticker"].asString();
        std::string direction = signal["signal"]["guidance_direction"].asString();
        double sentiment_score = signal["sentiment"]["score"].asDouble();
        
        double kelly_fraction = (2 * sentiment_score - 1) * 0.25;
        double position_size = cash_balance * std::max(0.0, kelly_fraction);
        
        if (direction == "raised" && sentiment_score > 0.7) {
            int shares = static_cast<int>(position_size / 100);
            if (shares > 0 && cash_balance >= shares * 100.0) {
                Position pos;
                pos.ticker = ticker;
                pos.quantity = shares;
                pos.entry_price = 100.0;
                pos.current_price = 100.0;
                
                positions.push_back(pos);
                cash_balance -= shares * 100.0;
                
                std::cout << "✅ BUY: " << shares << " shares of " << ticker 
                          << " @ $100 (Sentiment: " << sentiment_score << ")" << std::endl;
            }
        } 
        else if (direction == "lowered" && sentiment_score < 0.3) {
            for (auto it = positions.begin(); it != positions.end(); ++it) {
                if (it->ticker == ticker) {
                    double exit_price = 100.0;
                    double pnl = it->quantity * (exit_price - it->entry_price);
                    cash_balance += it->quantity * exit_price;
                    
                    std::cout << "✅ SELL: " << it->quantity << " shares of " << ticker 
                              << " @ $" << exit_price << " (P&L: $" << pnl << ")" << std::endl;
                    
                    positions.erase(it);
                    break;
                }
            }
        }
    }
    
    PerformanceMetrics calculateMetrics() {
        PerformanceMetrics metrics = {0, 0, 0};
        
        double portfolio_value = cash_balance;
        for (const auto& pos : positions) {
            portfolio_value += pos.quantity * pos.current_price;
        }
        
        metrics.total_pnl = portfolio_value - initial_capital;
        
        if (equity_curve.size() > 1) {
            double mean_return = 0;
            double variance = 0;
            
            for (size_t i = 1; i < equity_curve.size(); ++i) {
                double daily_return = (equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1];
                mean_return += daily_return;
            }
            mean_return /= (equity_curve.size() - 1);
            
            for (size_t i = 1; i < equity_curve.size(); ++i) {
                double daily_return = (equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1];
                variance += (daily_return - mean_return) * (daily_return - mean_return);
            }
            variance /= (equity_curve.size() - 1);
            
            double std_dev = std::sqrt(variance);
            if (std_dev > 0) {
                metrics.sharpe_ratio = mean_return * std::sqrt(252) / std_dev;
            }
        }
        
        double peak = initial_capital;
        double max_dd = 0;
        for (double value : equity_curve) {
            if (value > peak) peak = value;
            double drawdown = (peak - value) / peak;
            if (drawdown > max_dd) max_dd = drawdown;
        }
        metrics.max_drawdown = max_dd;
        
        return metrics;
    }
    
    void run(const std::vector<std::string>& headlines) {
        std::cout << "\n🚀 Trading Engine Started\n";
        std::cout << "Initial Capital: $" << initial_capital << "\n\n";
        
        for (const auto& headline : headlines) {
            std::cout << "📰 Processing: " << headline << "\n";
            
            Json::Value signal = analyzeHeadline(headline);
            if (!signal.empty()) {
                executeTrade(signal);
            }
            
            double current_value = cash_balance;
            for (const auto& pos : positions) {
                current_value += pos.quantity * pos.current_price;
            }
            equity_curve.push_back(current_value);
            
            std::cout << "💰 Portfolio: $" << current_value << "\n\n";
        }
        
        PerformanceMetrics metrics = calculateMetrics();
        printMetrics(metrics);
    }
    
    void printMetrics(const PerformanceMetrics& metrics) {
        std::cout << "\n" << std::string(50, '=') << "\n";
        std::cout << "📊 PERFORMANCE METRICS\n";
        std::cout << std::string(50, '=') << "\n";
        std::cout << "Total P&L:        $" << metrics.total_pnl << "\n";
        std::cout << "Sharpe Ratio:     " << metrics.sharpe_ratio << "\n";
        std::cout << "Max Drawdown:     " << (metrics.max_drawdown * 100) << "%\n";
        std::cout << std::string(50, '=') << "\n";
    }
};

int main() {
    TradingEngine engine("http://localhost:8000", 10000.0);
    
    std::vector<std::string> headlines = {
        "Apple raises Q4 guidance as iPhone 15 demand exceeds expectations",
        "Tesla cuts 2024 profit forecast amid competition",
        "Microsoft announces record cloud revenue growth",
        "Amazon reports better-than-expected earnings",
        "Meta slashes Q3 spending forecast significantly"
    };
    
    engine.run(headlines);
    
    return 0;
}
