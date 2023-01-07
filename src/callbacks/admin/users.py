from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    await callback_query.message.edit_text(
        text=constants.language.user_management,
        reply_markup=markups.create([
            (constants.language.user_profile, f"{constants.JSON_ADMIN}user_profile"),
            (constants.language.notify_everyone, f"{constants.JSON_ADMIN}notify_everyone"),
            (constants.language.back, f"{constants.JSON_ADMIN}adminPanel"),
        ])
    )


