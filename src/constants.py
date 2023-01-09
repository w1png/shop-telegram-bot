import importlib

import aiogram
from config import config
import os
import asyncio

if not os.path.exists("config.json"):
    config.init()
    
language = importlib.import_module(f"localization.{config['settings']['language']}")

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
STATUS_DICT = {
    0: language.status_processing,
    1: language.status_delivery,
    2: language.status_done,
    -1: language.status_cancelled,
}

JSON_USER = '{"r": "user"}'
JSON_MANAGER = '{"r": "manager"}'
JSON_ADMIN = '{"r": "admin"}'

loop = asyncio.new_event_loop()

bot = None
def create_bot(token: str) -> aiogram.bot.bot.Bot:
    global bot
    bot = aiogram.Bot(token=token, loop=loop)
    return bot

