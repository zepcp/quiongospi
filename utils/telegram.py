import settings

import requests
import os

def get_url(bot):
    if bot.lower() == "zomicbot":
        return settings.ZOMICBOT_URL
    if bot.lower() == "bebot":
        return settings.BEBOT_URL
    return None

def send_sticker(file_id, chat_id, bot="zomicbot"):
    url = os.path.join(get_url(bot),
                       "sendSticker")
    params = {"sticker": file_id,
              "chat_id": chat_id}

    res = requests.get(url, params=params)

    if res.status_code == 200:
        return res.json()['ok']
    return False

def send_photo(file_id, chat_id, caption=None, bot="zomicbot"):
    url = os.path.join(get_url(bot),
                       "sendPhoto")
    params = {"photo": file_id,
              "chat_id": chat_id,
              "caption": caption}

    res = requests.get(url, params=params)

    if res.status_code == 200:
        return res.json()['ok']
    return False

def send_message(text, chat_id, bot="zomicbot"):
    url = os.path.join(get_url(bot),
                       "sendMessage")
    params = {"text": text,
              "chat_id": chat_id}

    res = requests.get(url, params=params)

    if res.status_code == 200:
        return res.json()['ok']
    return False

def get_messages(offset = 0, bot="zomicbot"):
    url = os.path.join(get_url(bot),
                       "getUpdates")
    res = requests.get(url, params={"offset": offset})

    if res.status_code == 200:
        return res.json()["result"]
    return False

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)
