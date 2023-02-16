from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import re
import states


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", message.text):
        await callback_query.answer(constants.language.invalid_email)
        return

    await state.update_data(email=message.text)

    checkout_settings = constants.config["checkout_settings"]
    markup = [
        (constants.language.back, f'{{"r":"user","d":"cart"}}cancel')
    ]
    text = constants.language.unknown_error
    if checkout_settings["phone"]:
        text = constants.language.input_phone
        await states.Order.phone_number.set()
    elif checkout_settings["address"]:
        text = constants.language.input_address
        await states.Order.adress.set()
    elif checkout_settings["captcha"]:
        text = constants.language.input_captcha
        markup = [(constants.language.refresh, f'{{"r":"user"}}refresh')] + markup
        await states.Order.captcha.set()
    else:
        text = constants.language.input_comment
        await states.Order.comment.set()

    await callback_query.message.edit_text(
        text=text,
        reply_markup=markups.create(markup)
    )


