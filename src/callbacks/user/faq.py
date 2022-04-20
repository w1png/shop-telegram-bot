from aiogram import Bot
from users import User

from markups import markups
from constants import language

async def execute(bot: Bot, user: User, message_id: int, data: dict):
    await bot.edit_message_text(
       chat_id=user.id,
       message_id=message_id,
       text=language.faq,
       reply_markup=markups.faq
    ) 

