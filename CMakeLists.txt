cmake_minimum_required(VERSION 3.10)
project(TradingEngine)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(CURL REQUIRED)

# Manually set jsoncpp paths for macOS
set(JSONCPP_INCLUDE_DIRS "/opt/homebrew/Cellar/jsoncpp/1.9.8/include")
set(JSONCPP_LIB_DIR "/opt/homebrew/Cellar/jsoncpp/1.9.8/lib")

add_executable(trading_engine src/client/trading_engine.cpp)

target_include_directories(trading_engine PRIVATE 
    ${CURL_INCLUDE_DIRS}
    ${JSONCPP_INCLUDE_DIRS}
)

target_link_directories(trading_engine PRIVATE ${JSONCPP_LIB_DIR})

target_link_libraries(trading_engine 
    ${CURL_LIBRARIES}
    jsoncpp
)
