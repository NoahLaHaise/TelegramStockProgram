// DataAnalysisEngine.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>
#include <cstdlib>
#include <math.h>
#include "StockVect.h"

const std::string CSV_FOLDER = "C:\\pythonPrograms\\C++StockEngine\\CMake-StockProgram\\CSV_Files";
const std::string PY_FILE_PATH = "C:\\pythonPrograms\\C++StockEngine\\CMake-StockProgram\\Python\\stockPrices.py";

class DataAnalysis
{
public:
    std::string csv_path = "";
    std::vector<StockVect> data_vect;
    float mean_return;
    float mean_closing_price;
    float total_std;

    DataAnalysis(std::string file_path)
    {
        csv_path = file_path;

        read_file();
        calculate_mean();
        calculate_std();

        if (total_std)
        {
        }
    }

    void read_file()
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

    void calculate_mean()
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
        mean_return = return_sum / data_vect.size();

        std::cout << "\nClosing mean: " << mean_closing_price << " Return Mean: " << mean_return;
    }

    void calculate_std()
    {
        float diff_summed = 0;

        for (const auto &rec : data_vect)
        {
            float diff = rec.day_percent - mean_return;

            diff_summed += diff * diff;
        }

        total_std = sqrt(diff_summed / (data_vect.size() - 1));

        std::cout << "Standard Deviation: " << total_std;
    }
};

int main()
{
    std::string stock_symbol = "";
    std::cout << "Enter a Stock symbol to Analyze: ";
    std::cin >> stock_symbol;

    std::string csv_file = CSV_FOLDER + "\\" + stock_symbol + ".csv";

    std::ifstream fin(csv_file);
    int exit_code = 0;

    if (!fin)
    {
        std::string command = "python " + PY_FILE_PATH + " " + stock_symbol;

        exit_code = std::system(command.c_str());

        std::cout << "command ran: " << exit_code << " " << stock_symbol;
    }

    if (exit_code == 0)
    {
        std::cout << "Running Analysis";

        DataAnalysis data(csv_file);
    }
}
