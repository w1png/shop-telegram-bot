import importlib
from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    if not message.text.isdigit():
        await importlib.import_module("callbacks.admin.payment_settings").execute(callback_query, user, data, message)
        return
    constants.config.set(("delivery", "price"), int(message.text))

    await state.finish()
    await importlib.import_module("callbacks.admin.payment_settings").execute(callback_query, user, data, message)

