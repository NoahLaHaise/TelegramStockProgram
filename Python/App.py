from API.TelegramMessenger import TelegramMessenger
from API.GeminiAPI import GeminiAPI
import StockScreener
from WATCHLIST import WATCHLIST
from Prompts.PromptBuilder import message_prompt
from datetime import date, datetime

def send_alert():
    tele = TelegramMessenger()
    msg = StockScreener.watchlist_updates()
    tele.send_message(msg)

def daily_chat():
    tele = TelegramMessenger()
    gemini = GeminiAPI()
    print("chatting with gemini...")
    msg = gemini.chat_message(message_prompt)
    #print(msg)
    print("sending to tele...")
    tele.send_message(msg)

def app_runner():
    send_alert()

    now = datetime.now()
    if (now.hour == 16 and now.minute >= 25 and now.minute <= 59) or (now.hour == 11 and now.minute >= 29 and now.minute <= 59):
        daily_chat() 

def telegram_polling():
    """
    Not currently implemented
    """
    tele = TelegramMessenger()
    offset = 0
    while True:
        updates = tele.get_messages(offset=offset)
        for update in updates:
            offset = update['update_id'] + 1
            message = update['message']['text']
            print(f"Received message: {message}")
        

if __name__ == "__main__":
    app_runner()