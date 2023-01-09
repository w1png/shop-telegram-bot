from aiogram import types
import models
import constants
from markups import markups
import models
import asyncio
import time


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    text = constants.language.catalogue

    categories = await models.categories.get_main_categories()
    names = await asyncio.gather(*[category.name for category in categories])
    markup = markups.create([
        (name, f'{{"r":"user","cid":{category.id}}}category')
        for name, category in zip(names, categories)
    ])

    if message:
        return await message.answer(text, reply_markup=markup)
    await callback_query.message.edit_text(text, reply_markup=markup)


