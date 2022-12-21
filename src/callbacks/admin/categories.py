from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    await callback_query.message.edit_text(
        text=constants.language.category_management,
        reply_markup=markups.create([
            (constants.language.add_category, f"{constants.JSON_ADMIN}addCategory"),
            (constants.language.edit_category, f"{constants.JSON_ADMIN}editCategory"),
            (constants.language.back, f"{constants.JSON_ADMIN}adminPanel"),
        ])
    )


