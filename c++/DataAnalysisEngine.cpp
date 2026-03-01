// DataAnalysisEngine.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <math.h>
#include "Stock_Analysis/DataAnalysis.h"

#include <filesystem>
#include "API_Connections/TelegramMessenger.h"

namespace fs = std::filesystem;

const fs::path CSV_FOLDER = fs::path(PROJECT_ROOT_DIR) / "CSV_Files";
const fs::path PY_FILE_PATH = fs::path(PROJECT_ROOT_DIR) / "Python" / "CSV_stockPrices.py";
const fs::path PY_VENV_PATH = fs::path(PROJECT_ROOT_DIR) / "env" / "bin" / "python";
const fs::path CONFIG_PATH = fs::path(PROJECT_ROOT_DIR) / "config.json";

/*
FEATURES TO ADD

Send texts for stock updates once every 30 minutes for a list of given stocks.
Add alerts for when a stock breaks out of its moving average and when a stock hits its 200 week SMA


solidify Sharpe ratio calc + add support for multiple stock sharpe ratio

*/

// here symbol is being passed by reference
int pull_stock_data(const std::string &symbol)
{
    std::string run_py_script = std::string(PY_VENV_PATH) + " " + std::string(PY_FILE_PATH) + " " + symbol;

    std::cout << "\n\nCommand: " << run_py_script;

    return std::system(run_py_script.c_str());
}

DataAnalysis stock_engine()
{
    std::string stock_symbol = "";
    std::cout << "Enter a Stock symbol to Analyze: ";
    std::cin >> stock_symbol;
    const fs::path csv_file_path = CSV_FOLDER / "LongTerm" / std::string(stock_symbol + ".csv");
    std::ifstream stock_file(csv_file_path);

    std::cout << "FilePath: \n" << csv_file_path;

    int exit_code = 0;

    if (!stock_file)
        exit_code = pull_stock_data(stock_symbol); // add mode for short term or longterm data
    
    if (exit_code != 0)
        throw std::runtime_error("ERROR OCCURED WHEN GATHERING STOCK DATA");
    
    std::cout << "Running Analysis";
    DataAnalysis data(csv_file_path, stock_symbol);
    return data;
}

int main()
{
    DataAnalysis stock_data = stock_engine();

    std::string telegram_msg = stock_data.STOCK_SYMBOL + " Mean Closing Price: " + std::to_string(stock_data.get_mean_closing_price());

    TelegramMessenger TelegramMessenger(telegram_msg, CONFIG_PATH.string());
    TelegramMessenger.format_and_send();

}
