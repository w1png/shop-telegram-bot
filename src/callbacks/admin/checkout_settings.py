from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    checkout_data = constants.config["checkout"]
    captcha_sym = constants.language.tick if checkout_data["captcha"] else constants.language.cross
    email_sym = constants.language.tick if checkout_data["email"] else constants.language.cross
    phone_sym = constants.language.tick if checkout_data["phone"] else constants.language.cross

    markup = markups.create([
        (constants.language.payment_settings, f"{constants.JSON_ADMIN}payment_settings"),
        (constants.language.change_delivery_price, f"{constants.JSON_ADMIN}deliveryPrice"),

        (captcha_sym + constants.language.toggle_captcha, f"{constants.JSON_ADMIN}toggle_captcha"),
        (email_sym + constants.language.toggle_email, f"{constants.JSON_ADMIN}toggle_email"),
        (phone_sym + constants.language.toggle_phone_number, f"{constants.JSON_ADMIN}toggle_phone_number"),

        (constants.language.back, f"{constants.JSON_ADMIN}settings"),
    ])
    text = constants.language.checkout_settings

    if message:
        await message.answer(text, reply_markup=markup)
        return
    await callback_query.message.edit_text(
        text=text,
        reply_markup=markup
    )


