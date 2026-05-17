from API.TelegramMessenger import TelegramMessenger
from API.GeminiAPI import GeminiAPI
import StockScreener
from WATCHLIST import WATCHLIST
from Prompts.PromptBuilder import message_prompt

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

