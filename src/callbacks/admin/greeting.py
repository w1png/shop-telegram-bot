from aiogram import types
import models
import constants
from markups import markups
import states


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    await callback_query.message.edit_text(
        text=constants.language.input_greeting,
        reply_markup=markups.create([
            (constants.language.back, f'{{"r":"admin","d":"main_settings"}}cancel')
        ])
    )

    await states.Greeting.greeting.set()


