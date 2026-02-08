#pragma once
#include <string>
#include <vector>
#include "StockVect.h"

class DataAnalysis
{
public:
    const float RISK_FREE_RATE = .0424;
    std::string csv_path = "";
    const std::string STOCK_SYMBOL;
    DataAnalysis(const std::string &file_path, const std::string &symbol);
    void read_file();
    void calc_mean();
    void calc_std();
    void calc_sharpe();
    float get_mean_closing_price();

private:
    std::vector<StockVect> data_vect;
    float mean_day_return;
    float mean_closing_price;
    float total_std;
    float sharpe_ratio;
    float stocks_total_return;
};