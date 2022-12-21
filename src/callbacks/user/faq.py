from aiogram import types
import models
from markups import markups
import constants

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    markup = markups.create([
        (constants.language.contacts, f'{constants.JSON_USER}contacts'),
        (constants.language.refund_policy, f'{constants.JSON_USER}refund'),
    ])
    text = constants.language.faq

    if message:
        return await message.answer(text, reply_markup=markup)
    await callback_query.message.edit_text(text, reply_markup=markup)
    

