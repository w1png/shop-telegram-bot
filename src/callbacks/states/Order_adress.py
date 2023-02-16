from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    await state.update_data(adress=message.text)

    await callback_query.message.edit_text(
        text=constants.language.input_comment,
        reply_markup=markups.create([
            (constants.language.skip, f'{{"r":"user"}}skip'),
            (constants.language.back, f'{{"r":"user","d":"cart"}}cancel')
        ])
    )

