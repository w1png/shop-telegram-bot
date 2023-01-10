import importlib
from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    payment_methods = list(map(lambda payment_method: payment_method.id, models.payment_methods.get_enabled_payment_methods()))
    user_payment_method = (await user.cart.payment_method)

    if user_payment_method.id == 0:
        payment_method_id = payment_methods[0]
    else:
        payment_method_id = payment_methods[(payment_methods.index((await user.cart.payment_method).id) + 1) % len(payment_methods)]
    await user.cart.set_payment_method_id(payment_method_id)

    await importlib.import_module(f"callbacks.user.cart").execute(callback_query, user, data)

