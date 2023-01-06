from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import importlib

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    state_data = await state.get_data()
    category = models.categories.Category(state_data["category_id"])

    await category.set_name(message.text)

    data = {"cid": state_data["category_id"]}
    await importlib.import_module("callbacks.admin.editCategory").execute(callback_query, user, data, message=message)


