from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
     await callback_query.message.edit_text(
        text=constants.language.settings,
        reply_markup=markups.create([
            (constants.language.main_settings, f"{constants.JSON_ADMIN}main_settings"),
            (constants.language.checkout_settings, f"{constants.JSON_ADMIN}checkout_settings"),
            (constants.language.system_settings, f"{constants.JSON_ADMIN}system_settings"),
            (constants.language.stats_settings, f"{constants.JSON_ADMIN}stats_settings"),
            (constants.language.back, f"{constants.JSON_ADMIN}adminPanel"),
        ])
    )


