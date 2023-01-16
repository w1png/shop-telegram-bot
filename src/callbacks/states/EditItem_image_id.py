from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import importlib


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    state_data = await state.get_data()
    item = models.items.Item(state_data["item_id"])

    if callback_query:
        call = callback_query.data[callback_query.data.index("}")+1:]
        if call != "deleteItemImage":
            return
        await item.set_image_id("")
    else:
        image_id = message.photo[-1].file_id
        await item.set_image_id(image_id)

    data = {"iid": item.id}
    await importlib.import_module("callbacks.admin.editItem").execute(callback_query, user, data, message=message)


