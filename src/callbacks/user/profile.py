from aiogram import types
import models
import constants
from markups import markups
import asyncio


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    username, registration_date, is_admin, is_manager = await asyncio.gather(
        user.username,
        user.date_created,
        user.is_admin,
        user.is_manager
    )

    markup = [
        (constants.language.orders, f"{constants.JSON_USER}orders"),
    ]

    text = constants.language.format_user_profile(
        id=user.id,
        username=username,
        registration_date=registration_date,
        is_admin=is_admin,
        is_manager=is_manager
    )

    if message:
        return await message.answer(text=text, reply_markup=markups.create(markup))
    await callback_query.message.edit_text(text=text, reply_markup=markups.create(markup))


