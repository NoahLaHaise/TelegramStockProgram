#pragma once
#include <string>


//header files are needed to #include this class into other files. For simple classes like vectorStructure.cpp we actually only need the header
struct StockVect
{
    std::string record_date;
    float open_price;
    float close_price;
    float volume;
    float day_percent;

};