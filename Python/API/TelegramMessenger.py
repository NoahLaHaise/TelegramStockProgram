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

        print(f"\nsending message to tele: {msg}")
        url = f'{self.endpoint}/sendMessage'

        msg_blocks = [msg[i:i+4096] for i in range(0, len(msg), 4096)]
        for msg in msg_blocks:
            payload = {
                'chat_id': self.chat_id,
                'text': msg,
            }

            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
            except Exception as e:
                print(f"can't send messages to tele: {e}")

    def get_messages(self, offset: int = 0, timeout: int = 30):
        url = f'{self.endpoint}/getUpdates'
        try:
            
            response = requests.get(url, params= {'offset': offset, 'timeout': timeout})
            response.raise_for_status()
        except Exception as e:
            print(f"can't get messages from tele: {e}")

# tele = TelegramMessenger()
# tele.get_messages()