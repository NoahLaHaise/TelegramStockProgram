#include "SqlLite.h"
#include <iostream>
#include <sqlite3.h>

SqlConnector::SqlConnector(const std::string &db_name)
    : database_name(db_name) {
  sqlite3 *db = get_connection();
  if (!db) {
    std::cerr << "db connection failed";
    return;
  }
  char *errMsg = nullptr;

  const char *sql = "CREATE TABLE IF NOT EXISTS stock_analysis ("
                    "id   INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "stock TEXT NOT NULL,"
                    "day_200_mean REAL,"
                    "day_50_mean REAL,"
                    "sharpe_ratio REAL"
                    ");";

  if (sqlite3_exec(db, sql, nullptr, nullptr, &errMsg) != SQLITE_OK) {
    std::cerr << "Create table failed: " << errMsg << "\n";
    sqlite3_free(errMsg);
  }
  sqlite3_close(db);
}
sqlite3 *SqlConnector::get_connection() {
  sqlite3 *db;
  int rc = sqlite3_open(database_name.c_str(),
                        &db); // Creates file if it doesn't exist

  if (rc != SQLITE_OK) {
    sqlite3_close(db);
    return nullptr;
  }
  return db;
}

bool SqlConnector::insert_record(std::string stock_symbol, float large_sma,
                                 float small_sma, float sharpe_ratio) {
  sqlite3 *db = get_connection();
  if (!db) {
    std::cerr << "db connection failed";
    return false;
  }

  sqlite3_stmt *stmt;

  sqlite3_prepare_v2(db,
                     "INSERT INTO stock_analysis (stock, day_200_mean, "
                     "day_50_mean, sharpe_ratio) VALUES (?, ?, ?, ?);",
                     -1, &stmt, nullptr);

  sqlite3_bind_text(stmt, 1, stock_symbol.c_str(), -1, SQLITE_STATIC);
  sqlite3_bind_double(stmt, 2, large_sma);
  sqlite3_bind_double(stmt, 3, small_sma);
  sqlite3_bind_double(stmt, 4, sharpe_ratio);

  if (sqlite3_step(stmt) != SQLITE_DONE) {
    std::cerr << "Insert failed: " << sqlite3_errmsg(db) << "\n";
    sqlite3_finalize(stmt);
    sqlite3_close(db);

    return false;
  }

  sqlite3_finalize(stmt);
  sqlite3_close(db);
  return true;
}
