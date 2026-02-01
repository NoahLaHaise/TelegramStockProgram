#from turtle import save
import yfinance as yf
import pendulum
import matplotlib.pyplot as plt
import pandas as pd
import config
import sys
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

    #def priceHistory(self, history):
        #print(self.stockHistory)
        #for price in self.price:
            #print()
       #self.stockHistory = history


def main(stockName: str):

    #stockName = input("Enter the Stock Ticker you want information on: ")
    stock_info = yf.Ticker(stockName).info

    price_history = yf.Ticker(stockName).history(period='3y', # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                   interval='1d', # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                                   actions=False)
    

    currStock = Stock(stockName, stock_info.get('currentPrice'), stock_info.get('earningsGrowth'), stock_info.get('profitMargins'), stock_info.get('ebitdaMargins'), stock_info.get('returnOnEquity'), stock_info.get('trailingEps'), stock_info.get('beta'), stock_info.get('pegRatio'), stock_info.get('totalCash'), stock_info.get('totalDebt'), stock_info.get('quickRatio'), price_history)  
    
   # graphOrCalc = input("Enter 1 to generate graph, Enter 2 to calculate price prediction, Enter 3 to generate recent news: ")


    price_history['Return'] = (price_history['Close'] - price_history['Open']) / price_history['Open']
    price_history.drop(columns=['Low', 'High'], inplace=True)
    price_history[['Open', 'Close', 'Return']] = price_history[['Open', 'Close', 'Return']].round(4)
    #print(price_history)

    #if input("Would you like to save the price history to a CSV file? (y/n): ").lower() == 'y':
    save_to_csv(price_history, stockName)


def save_to_csv(stock_history : pd.DataFrame, stock_name: str):
    stock_history.to_csv(f"{config.CSV_FILE_PATH}\{stock_name}.csv")

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


def displayInfo(stockInfo : Stock, name : str)-> None:
    print("Valid periods include: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max\n")
    per = input("Enter the period of time you would like your graph: ")
    print("\n valid intervals include: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo")
    inter = input("Enter the interval of prices you would: ")

    price_history = yf.Ticker(name).history(period=per, # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                                   interval= inter, # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                                   actions=False)

    print(stockInfo.name, ' ', stockInfo.price)

    timeSeries = list(price_history['Open'])
    dt_list = [pendulum.parse(str(dt)).float_timestamp for dt in list(price_history.index)]

    plt.style.use('dark_background')
    plt.plot(dt_list, timeSeries, linewidth=2)

    plt.show()


if len(sys.argv) > 1:
    stock = sys.argv[1]
    main(stock)