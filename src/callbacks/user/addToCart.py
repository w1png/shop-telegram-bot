from aiogram import Bot
from importlib import import_module

from users import User
from items import Item

async def execute(bot: Bot, user: User, message_id: int, data: dict):
    item = Item(data["item_id"])
    user.cart.items.add(item)
    
    await import_module(f"callbacks.user.{data['dest']}").execute(bot, user, message_id, data)

