from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    await callback_query.message.edit_text(
        text=constants.language.item_management,
        reply_markup=markups.create([
            (constants.language.add_item, f"{constants.JSON_ADMIN}add_item"),
            (constants.language.edit_item, f"{constants.JSON_ADMIN}edit_items"),
            (constants.language.back, f"{constants.JSON_ADMIN}adminPanel")
        ])
    )


