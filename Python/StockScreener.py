from finvizfinance.quote import finvizfinance
from tradingview_screener import Query, col
from datetime import datetime, timedelta
import pandas as pd
from WATCHLIST import WATCHLIST
import yfinance as yf
from API.TelegramMessenger import TelegramMessenger
#pull news from finviz finvizfinance 

#screen for stocks with tradingview tradingview-screener

def stock_scanner():

    df = (Query()
          .select('name', 'volume', 'change_abs', 'change')
          .where(col('volume') > 5_000_000, 
                 col('change') > 2,
                 col('exchange').isin(['NASDAQ', 'NYSE']))
          .limit(25)
          .order_by('change', ascending=False)
          .get_scanner_data())
    
    print(df)

def stock_news():
    #finviz and yfinance news seem to return quite a bit of slop
    stock = finvizfinance('GOOGL')
    news_results = stock.ticker_news()
    news_results["Date"] = pd.to_datetime(news_results["Date"])
    news_results = news_results[news_results["Date"] >  datetime.now() - timedelta(hours=24)]
    print(news_results)

def watchlist_updates() -> str:
    updates = ""
    for ticker in WATCHLIST:
        price_history = yf.Ticker(ticker).history(period='1d', 
                                                  interval='30m', 
                                                  actions=False)
        
        #print(price_history)
        price_movement = price_history.tail(2)['Close']
        percent_change = price_movement.pct_change().iloc[1]

        updates += f"Ticker: {ticker} has moved {percent_change:.2%}. Current price {round(price_movement.iloc[1], 2)}\n"

    return updates

    
#watchlist_updates()
#stock_scanner()
    