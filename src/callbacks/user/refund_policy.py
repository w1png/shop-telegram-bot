from aiogram import Bot, types
from users import User

from config import config
from constants import language, JSON_USER

async def execute(bot: Bot, user: User, message_id: int, data: dict):
   await bot.edit_message_text(
       chat_id=user.id,
       message_id=message_id,
       text=config["info"]["refund_policy"],
       reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text=language.back, callback_data=f"{JSON_USER}faq"))
    )

