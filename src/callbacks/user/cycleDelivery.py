import importlib
from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    await user.cart.set_delivery_id(int(not await user.cart.delivery_id))

    await importlib.import_module("callbacks.user.cart").execute(callback_query, user, data)


