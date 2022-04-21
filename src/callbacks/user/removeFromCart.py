from aiogram import Bot
from importlib import import_module

from users import User
from items import Item 

async def execute(bot: Bot, user: User, message_id: int, data: dict):
    item = Item(data["item_id"])
    user.cart.items.remove(item)

    await import_module("callbacks.user.item").execute(bot, user, message_id, data)

