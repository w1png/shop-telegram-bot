import importlib
from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    call = callback_query.data[callback_query.data.index("}")+1:]
    state_data = await state.get_data()

    category = models.categories.Category(state_data["category_id"])
    await category.set_parent_id(data["pid"])

    data["cid"] = state_data["category_id"]
    await importlib.import_module("callbacks.admin.editCategory").execute(callback_query, user, data)

