from aiogram import Bot, types

from users import User
from categories import Category
from items import Item
from constants import language, JSON_USER
from markups import markups

async def execute(bot: Bot, user: User, message_id: int, data: dict):
    category = Category(data["category_id"])

    buttons = list()
    for item_id in category.items:
        item = Item(item_id)
        buttons.append((item.name, f'{{"role": "user", "item_id": {item.id}}}item'))
    buttons.append((language.back, f'{JSON_USER}catalogue'))

    await bot.edit_message_text(
       chat_id=user.id,
       message_id=message_id,
       text=category.name,
       reply_markup=markups.create(buttons)
    ) 

