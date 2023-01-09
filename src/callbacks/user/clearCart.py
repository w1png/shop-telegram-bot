from aiogram import types
import models
import constants
from markups import markups
import importlib


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    await user.cart.items.clear()

    await importlib.import_module("callbacks.user.cart").execute(callback_query, user, data)


