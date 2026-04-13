from API.TelegramMessenger import TelegramMessenger
from API.GeminiAPI import GeminiAPI
import StockScreener
from WATCHLIST import WATCHLIST

def send_alert():
    tele = TelegramMessenger()
    msg = StockScreener.watchlist_updates()
    tele.send_message(msg)

def daily_chat():
    #TODO - pass in VWAP, RSI, moving averages 
    tele = TelegramMessenger()
    prompt = f"Provide an update on my stock portfolio for each individual stock. How is the price action today? Why are they moving? Are they moving because of the broader market? Or independent news? Provide an overview on the overall market structure and sentiment as well. If theres any major market wide news or company specific news that affect their future outlook, be sure to highlight it. {' '.join(WATCHLIST)}"
    gemini = GeminiAPI()
    print("chatting with gemini...")
    msg = gemini.chat_message(prompt)


    #print(msg)
    print("sending to tele...")
    tele.send_message(msg)

def app_runner():
    while True:
        print('hi')

        send_alert()

        #if sql db lookup last ai alert sent 60 minutes ago
            # daily_chat()

        # if 430pm EST, send daily briefing

# run this with a cron job
#send_alert()
daily_chat()
#app_runner()

