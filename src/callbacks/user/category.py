from aiogram import Bot
from users import User
from categories import Category
from items import Item
from aiogram import types
from constants import language, JSON_USER

async def execute(bot: Bot, user: User, message_id: int, data: dict):
    category = Category(data["category_id"])

    markup = types.InlineKeyboardMarkup()
    for item_id in category.items:
        item = Item(item_id)
        markup.add(types.InlineKeyboardButton(text=item.name, callback_data=f'{{"role": "user", "item_id": {item.id}}}item'))
    markup.add(types.InlineKeyboardButton(text=language.back, callback_data=f'{JSON_USER}catalogue'))

    await bot.edit_message_text(
       chat_id=user.id,
       message_id=message_id,
       text=category.name,
       reply_markup=markup
    ) 

