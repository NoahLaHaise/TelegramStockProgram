#pragma once
#include <sqlite3.h>
#include <string>

class SqlConnector {
public:
  SqlConnector(const std::string &db_name);
  const std::string &database_name;
  bool insert_record(std::string stock_symbol, float large_sma, float small_sma,
                     float sharpe_ratio);
  bool select_record();
  sqlite3 *get_connection();
};
