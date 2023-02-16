from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import states
import re


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    if re.match(r"^(\+7|8)\d{10}$", message.text):
        await message.answer(constants.language.invalid_phone_number)
        return

    await state.update_data(phone_number=message.text)

    checkout_settings = constants.config['checkout']

    text = constants.language.unknown_error
    if checkout_settings["address"]:
        text = constants.language.input_address
        await states.Order.adress.set()
    else:
        text = constants.language.input_comment
        await states.Order.comment.set()

    await callback_query.message.edit_text(
        text=text,
        reply_markup=markups.create([
            (constants.language.back, f'{{"r":"user","d":"cart"}}cancel')
        ])
    )


