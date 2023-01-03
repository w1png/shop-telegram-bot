from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    call = callback_query.data[callback_query.data.index("}")+1:]

    constants.config.set(("settings", "language"), call)

    await callback_query.message.edit_text(
        text=constants.language.language_was_set,
        reply_markup=markups.create([
            (constants.language.back, f"{constants.JSON_ADMIN}main_settings")
        ])
    )
    
    await state.finish()
