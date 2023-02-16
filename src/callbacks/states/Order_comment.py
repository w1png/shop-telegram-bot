from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    await state.update_data(comment=message.text)
    data = await state.get_data()

    await callback_query.message.edit_text(
        text=constants.language.confirm_order(
            email=data["email"],
            phone_number=data["phone_number"],
            adress=data["adress"],
            comment=data["comment"],
        ),
        reply_markup=markups.create([
            (constants.language.back, f'{{"r":"user","d":"cart"}}cancel')
        ])
    )


