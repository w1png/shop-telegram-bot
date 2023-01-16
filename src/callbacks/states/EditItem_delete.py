from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import importlib


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    call = callback_query.data[callback_query.data.index("}")+1:]
    if call != "deleteItem":
        return

    state_data = await state.get_data()
    item = models.items.Item(state_data["item_id"])

    await item.delete()

    await state.finish()
    await callback_query.message.edit_text(
        text=constants.language.item_was_deleted,
        reply_markup=markups.create([
            (constants.language.back, f"{constants.JSON_ADMIN}items")
        ])
    )

