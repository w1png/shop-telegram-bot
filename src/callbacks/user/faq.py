from aiogram import Bot
import models
from markups import markups
import constants

async def execute(bot: Bot, user: models.user.User, message_id: int, data: dict):
    await bot.edit_message_text(
       chat_id=user.id,
       message_id=message_id,
       text=constants.language.faq,
       markup=markups.create([
            (language.contacts, f'{constants.JSON_USER}contacts'),
            (language.refund, f'{constants.JSON_USER}refund'),
        ])
    ) 

