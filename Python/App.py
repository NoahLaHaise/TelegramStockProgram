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

    datetime = datetime.now()
    if (datetime.hour == 16 and datetime.minute >= 25 and datetime.minute <= 59) or (datetime.hour == 12 and datetime.minute >= 0 and datetime.minute <= 32):
        daily_chat() 

def telegram_polling():
    tele = TelegramMessenger()
    offset = 0
    while True:
        updates = tele.get_messages(offset=offset)
        for update in updates:
            offset = update['update_id'] + 1
            message = update['message']['text']
            print(f"Received message: {message}")
        


# run this with a cron job
#send_alert()
#daily_chat()
app_runner()
#telegram_polling()
