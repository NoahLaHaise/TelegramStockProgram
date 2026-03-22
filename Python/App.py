from API.TelegramMessenger import TelegramMessenger
from API.GeminiAPI import chat_message
import StockScreener
from WATCHLIST import WATCHLIST

def send_alert():
    tele = TelegramMessenger()
    msg = StockScreener.watchlist_updates()
    tele.send_message(msg)

def daily_chat():
    tele = TelegramMessenger()
    prompt = f"Provide a high level update on my stock portfolio, for each individual stock. How is the price action today? Why are they moving? Are they moving because of the broader market? Or independent news? Provide an overview on the overall market structure and sentiment as well. {' '.join(WATCHLIST)}"

    msg = chat_message(prompt)
    print(msg)
    tele.send_message(msg)

def app_runner():
    while True:
        print('hi')

        send_alert()

        #if sql db lookup last ai alert sent 60 minutes ago
            # daily_chat()

        # if 430pm EST, send daily briefing

# run this with a cron job
app_runner()

