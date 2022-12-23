from aiogram import types
import models
import constants
from markups import markups
import models
import asyncio


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    text = constants.language.catalogue

    markup = markups.create([
        (await category.name, f'{{"r":"user","cid":{category.id}}}category')
        for category in await models.categories.get_main_categories()
    ])

    if message:
        return await message.answer(text, reply_markup=markup)
    await callback_query.message.edit_text(text, reply_markup=markup)


