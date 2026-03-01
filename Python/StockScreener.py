from finvizfinance.quote import finvizfinance
from tradingview_screener import Query, col
from datetime import datetime, timedelta
import pandas as pd
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
    stock = finvizfinance('GOOGL')
    news_results = stock.ticker_news()
    news_results["Date"] = pd.to_datetime(news_results["Date"])
    news_results = news_results[news_results["Date"] >  datetime.now() - timedelta(hours=24)]
    print(news_results)
    
stock_news()
#stock_scanner()
    