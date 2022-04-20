from aiogram import Bot, types
from users import User

from config import config
from constants import language, JSON_USER
from markups import markups

async def execute(bot: Bot, user: User, message_id: int, data: dict):
    await bot.edit_message_text(
       chat_id=user.id,
       message_id=message_id,
       text=config["info"]["contacts"],
       reply_markup=markups.create([(language.back, f"{JSON_USER}faq")])
    ) 

