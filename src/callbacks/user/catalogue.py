from aiogram import Bot
from users import User
from constants import language
from markups import markups
from categories import cat_list

async def execute(bot: Bot, user: User, message_id: int, data: dict):
   await bot.edit_message_text(
       chat_id=user.id,
       message_id=message_id,
       text=language.catalogue,
       reply_markup=markups.catalogue(cat_list())
   ) 

