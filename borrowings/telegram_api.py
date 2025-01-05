from dotenv import load_dotenv
import os
import telebot

load_dotenv()


class TelegramSender:
    def __init__(self):
        token = os.getenv("TELEGRAM_BOT__TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if token is None or chat_id is None:
            raise ValueError("TELEGRAM_BOT__TOKEN or TELEGRAM_CHAT_ID is not set in the environment variables")

        self.bot = telebot.TeleBot(token)
        self.chet_id = chat_id

    def send_message(self, text):
        try:
            self.bot.send_message(
                chat_id=self.chet_id, text=text, parse_mode="markdown"
            )
        except telebot.apihelper.ApiException as e:
            print(f"Error sending message to Telegram: {e}")


telegram_sender = TelegramSender()
