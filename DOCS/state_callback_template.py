from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> none:
    call = callback_query.data[callback_query.data.index("}")+1:]

    await state.update_data()
    data = await state.get_data()

    await callback_query.message.edit_text(
        text=constants.language.none,
        reply_markup=markups.create([

        ])
    )


