import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

class TelegramMessenger:
    message: str
    endpoint: str
    chat_id: int

    def __init__(self):
        self.endpoint = os.getenv("TELEGRAM_ENDPOINT")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def build_alert(self, stats: dict) -> str:
        message = ""
        for col in stats.keys():
            message += f"{col}: {round(stats[col], 2)}\n"
        return message
    
    def send_message(self, msg: str):

        url = f'{self.endpoint}/sendMessage?chat_id={self.chat_id}&text={quote(msg)}'
        try:
            requests.post(url)
        except:
            print("can't send messages to tele")

    def get_messages(self):
        url = f'{self.endpoint}/getUpdates'
        try:
            response = requests.get(url)
            print(response.text)
        except:
            print("can't get messages frpm tele")