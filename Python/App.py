from API.TelegramMessenger import TelegramMessenger
from API.GeminiAPI import chat_message
import StockScreener
from WATCHLIST import WATCHLIST

def send_text():
    tele = TelegramMessenger()
    msg = StockScreener.watchlist_updates()
    tele.send_message(msg)

def daily_chat():
    tele = TelegramMessenger()
    prompt = f"Provide a high level update on my stock portfolio, for each individual stock. How is the price action today? Why are they moving? Are they moving because of the broader market? Or independent news? Provide an overview on the overall market structure and sentiment as well. {' '.join(WATCHLIST)}"

    msg = chat_message(prompt)
    print(msg)
    tele.send_message(msg)

daily_chat()

