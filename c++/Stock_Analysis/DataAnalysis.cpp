#include "DataAnalysis.h"
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <math.h>

DataAnalysis::DataAnalysis(const std::string &file_path, const std::string &symbol)
    : csv_path(file_path), STOCK_SYMBOL(symbol), mean_day_return(0), mean_closing_price(0),
      total_std(0), sharpe_ratio(0), stocks_total_return(0)
{
    read_file();
    calc_mean();
    calc_std();
    calc_sharpe();
}



void DataAnalysis::read_file()
{
    std::ifstream csv_read(csv_path);
    std::string file_contents;

    if (csv_read.is_open())
    {

        bool first_line = true;
        while (std::getline(csv_read, file_contents))
        {

            if (first_line)
            {
                first_line = false;
                continue;
            }

            std::istringstream line(file_contents);
            std::string line_contents;

            StockVect tempvec;
            int i = 0;
            while (std::getline(line, line_contents, ','))
            {

                try
                {
                    switch (i)
                    {
                    case 0:
                        tempvec.record_date = line_contents;
                        break;
                    case 1:
                        tempvec.open_price = std::stof(line_contents);
                        break;
                    case 2:
                        tempvec.close_price = std::stof(line_contents);
                        break;
                    case 3:
                        tempvec.volume = std::stof(line_contents);
                        break;
                    case 4:
                        tempvec.day_percent = std::stof(line_contents);
                    default:
                        break;
                    }
                }
                catch (...)
                {
                    i++;
                    continue;
                }

                i++;
            }
            data_vect.push_back(tempvec);
            // std::cout << tempvec.record_date << " " << tempvec.close_price << "\n\n";
        }

        csv_read.close();
    }
}

void DataAnalysis::calc_mean()
{
    float close_sum = 0;
    float return_sum = 0;

    // read only reference to the StockVec record (not a copy)
    for (const auto &rec : data_vect)
    {
        close_sum += rec.close_price;
        return_sum += rec.day_percent;
    }

    mean_closing_price = close_sum / data_vect.size();
    mean_day_return = return_sum / data_vect.size();

    std::cout << "\nClosing mean: " << mean_closing_price << " Return Mean: " << mean_day_return;
}

void DataAnalysis::calc_std()
{
    float diff_summed = 0;

    for (const auto &rec : data_vect)
    {
        float diff = rec.day_percent - mean_day_return;

        diff_summed += diff * diff;
    }

    total_std = sqrt(diff_summed / (data_vect.size() - 1));

    std::cout << "\nStandard Deviation: " << total_std;
}

void DataAnalysis::calc_sharpe()
{
    /*
     * To make the sharpe ratio more accurate, we really need to smooth out the RISK_FREE_RATE over the time frame we are working with.
     * IE: if we calc for 3 years, then we need to smooth the risk free rate to be the average of 3month tbills across this period, or 1yr tbonds.
     */

    stocks_total_return = (data_vect.back().close_price - data_vect.front().close_price) / data_vect.back().close_price;

    sharpe_ratio = (stocks_total_return - RISK_FREE_RATE) / (total_std * sqrt(252));

    std::cout << "\nSharpe Ratio: " << sharpe_ratio << " Stocks return: " << stocks_total_return;
}

float DataAnalysis::get_mean_closing_price()
{
    return mean_closing_price;
}
