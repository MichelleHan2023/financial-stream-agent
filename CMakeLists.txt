cmake_minimum_required(VERSION 3.10)
project(FinancialStreamAgent)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(CURL REQUIRED)

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/src/include)

# Add trading engine executable
add_executable(trading_engine 
    src/client/trading_engine.cpp
)

# Link libraries
target_link_libraries(trading_engine 
    ${CURL_LIBRARIES}
)

# Installation
install(TARGETS trading_engine DESTINATION bin)

message(STATUS "✅ Financial Stream Agent - C++ Trading Engine")
message(STATUS "   Python components: Real-time signal generation")
message(STATUS "   C++ components: High-performance stream processing")
