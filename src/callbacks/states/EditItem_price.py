import importlib
from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    state_data = await state.get_data()
    item = models.items.Item(state_data["item_id"])

    if not message.text.replace(".", "", 1).replace(",", "", 1).isdigit():
        await message.answer("Цена должна быть числом")
        return

    price = message.text.replace(",", ".")

    await item.set_price(float(price))

    data = {"iid": item.id}
    await importlib.import_module("callbacks.admin.editItem").execute(None, user, data, message)


