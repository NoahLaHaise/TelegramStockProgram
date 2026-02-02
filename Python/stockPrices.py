#from turtle import save
import yfinance as yf
import pendulum
import matplotlib.pyplot as plt
import pandas as pd
import config
import sys
from pathlib import Path

#yf.set_tz_cache_location(None)
#print(stock_info)

from dataclasses import dataclass

@dataclass
class Stock:
    name: str
    price: float
    earningGrowth: float
    ebitdaMargin: float
    profitMargin: float
    ROE: float
    trailingEPS: float
    beta: float
    pegRatio: float
    totalCash: float
    totalDebt: float
    quickRatio: float
    priceHistory: list[float]

def get_longterm_history(stockName: str):
    price_history = yf.Ticker(stockName).history(period='3y', # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                   interval='1d', # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                                   actions=False)
    
    price_history['Return'] = (price_history['Close'] - price_history['Open']) / price_history['Open']
    price_history.drop(columns=['Low', 'High'], inplace=True)
    price_history[['Open', 'Close', 'Return']] = price_history[['Open', 'Close', 'Return']].round(4)

    save_to_csv(price_history, stockName)

def get_day_movement(stockName: str) -> None:
    price_history = yf.Ticker(stockName).history(period='1d', # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                interval='5m', # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                                actions=False)
    
    price_history.drop(columns=['Low', 'High', 'Open'], inplace=True)
    price_history[['Close']] = price_history[['Close']].round(4)
    save_to_csv(price_history, stockName, False, "ShortTerm") 

def save_to_csv(stock_history : pd.DataFrame, stock_name: str, time_frame: str = "LongTerm"):
    file_path = config.CSV_FILE_PATH / time_frame / f"{stock_name}.csv"
    stock_history.to_csv(file_path) #set index =False to remove dateTime

def generateNews(info, name) -> None:
    news = yf.Ticker(name).news
    link = news[1]

    #https://www.turing.com/kb/5-powerful-text-summarization-techniques-in-python
    for article in news:
        print(article['link'])

    #print(link['link'))
    
def calcDiscountModel(info, name)-> None:
#https://www.investopedia.com/terms/d/ddm.asp
    dividend = yf.Ticker(name).dividends

    print(dividend)

def calcBlackScholes(info, name)-> None:
    print("working")


if len(sys.argv) > 1:
    stock = sys.argv[1]

    if len(sys.argv) > 2:
        mode = sys.argv[2]
        if mode == "long":
            get_longterm_history(stock)
        else:
            get_day_movement(stock) 
            