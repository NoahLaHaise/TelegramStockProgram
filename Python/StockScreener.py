from finvizfinance.quote import finvizfinance
from tradingview_screener import Query, col
from datetime import datetime, timedelta
import pandas as pd
from WATCHLIST import WATCHLIST
import yfinance as yf
from API.TelegramMessenger import TelegramMessenger

def stock_scanner():

    df = (Query()
          .select('name', 'volume', 'change_abs', 'change')
          .where(col('volume') > 5_000_000, 
                 col('change') > 5,
                 col('exchange').isin(['NASDAQ', 'NYSE']))
          .limit(25)
          .order_by('change', ascending=False)
          .get_scanner_data())
    
    print(df)

def stock_indicators(ticker: str) -> str:
    _, df = (Query()
        .select('name', 'RSI', 'MACD.macd', 'MACD.signal', 'BB.upper', 'BB.lower')
        .where(col('name') == ticker).get_scanner_data())

    if df.empty:
        return "No indicator data found"

    row = df.iloc[0]
    return (f"RSI: {row['RSI']:.1f} | "
            f"MACD: {row['MACD.macd']:.2f} / Signal: {row['MACD.signal']:.2f} | "
            f"BB: {row['BB.lower']:.2f} - {row['BB.upper']:.2f}")

def watchlist_updates() -> str:
    updates = ""
    for ticker in WATCHLIST:
        price_history = yf.Ticker(ticker).history(period='1d', 
                                                  interval='30m', 
                                                  actions=False)
        
        price_movement = price_history.tail(2)['Close']
        print(price_movement)
        percent_change = price_movement.pct_change().iloc[1]

        updates += f"Ticker: {ticker} has moved {percent_change:.2%}. Current price {round(price_movement.iloc[1], 2)}\n "
        updates += f"Key indicators: {stock_indicators(ticker)}\n\n"

    return updates
