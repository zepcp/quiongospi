"""Telegram utils"""
import os
import requests

import settings

class BOT():
    """Telegram bot class, get and send info"""
    def __init__(self, bot="bebot"):
        self.base_url = settings.ZOMICBOT_URL if bot.lower() == "zomicbot" \
                        else settings.BEBOT_URL if bot.lower() == "bebot" \
                        else None

    def get_url(self, params=None):
        """Get Telegram URL"""
        if not params:
            return os.path.join(self.base_url, "getUpdates")
        query = "sendSticker" if "sticker" in params else \
               "sendPhoto" if "photo" in params else "sendMessage"
        return os.path.join(self.base_url, query)

    @staticmethod
    def get_params(chat, text=None, sticker=None, photo=None):
        """Parse sent info as params"""
        params = {"chat_id": chat}
        if sticker:
            params["sticker"] = sticker
        elif photo:
            params["photo"] = photo
            params["caption"] = text
        elif text:
            params["text"] = text
        return params

    def send(self, chat, text=None, sticker=None, photo=None):
        """Send info to telegram chat"""
        params = self.get_params(chat, text, sticker, photo)
        res = requests.get(self.get_url(params), params=params)
        #Cant send sticker and photo simultaneously
        if sticker and photo:
            params = self.get_params(chat, text, photo=photo)
            res = requests.get(self.get_url(params), params=params)
        #Cant send sticker and text simultaneously
        elif sticker and text:
            params = self.get_params(chat, text)
            res = requests.get(self.get_url(params), params=params)
        return res.json()["ok"] if res.status_code == 200 else False

    def get(self, offset=0):
        """Receive info sent to telegram bot"""
        res = requests.get(self.get_url(), params={"offset": offset})
        return res.json()["result"] if res.status_code == 200 else False