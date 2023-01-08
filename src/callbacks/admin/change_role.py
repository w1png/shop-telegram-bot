import importlib
from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    role = data["nr"]
    state = data["s"]
    edit_user = models.users.User(data["uid"])

    if role == "a":
        await edit_user.set_admin(state)
    elif role == "m":
        await edit_user.set_manager(state)

    data = {
        "uid": edit_user.id
    }

    await importlib.import_module("callbacks.states.UserProfile_id").execute(callback_query, user, data, message)


