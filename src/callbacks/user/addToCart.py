import importlib
from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    await user.cart.items.add(data['iid'])

    await importlib.import_module("callbacks.user.item").execute(callback_query, user, data)

