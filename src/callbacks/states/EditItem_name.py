import importlib
from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    state_data = await state.get_data()
    item = models.items.Item(state_data["item_id"])
    

    await item.set_name(message.text)

    data = {"iid": item.id}
    await importlib.import_module("callbacks.admin.editItem").execute(None, user, data, message)


