import importlib
from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    payment_method = models.payment_methods.PaymentMethod(data["pmid"])

    payment_method.set_enabled(not payment_method["enabled"])
    
    await importlib.import_module("callbacks.admin.payment_settings").execute(callback_query, user, data)

