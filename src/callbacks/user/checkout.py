from aiogram import types
import models
import constants
from markups import markups
import states


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    checkout_settings = constants.config['checkout']
    text = constants.language.unknown_error

    if checkout_settings["email"]:
        text = constants.language.input_email
        await states.Order.email.set()
    elif checkout_settings["phone"]:
        text = constants.language.input_phone
        await states.Order.phone_number.set()
    elif checkout_settings["address"]:
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


