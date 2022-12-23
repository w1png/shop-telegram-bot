from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    markup = [
        (f"[{category.id}] {await category.name}", f'{{"r":"admin","cid":{category.id}}}editCategory')
        for category in await models.categories.get_categories()
    ]
    markup.append((constants.language.back, f"{constants.JSON_ADMIN}categories"))

    await callback_query.message.edit_text(
        text=constants.language.edit_category,
        reply_markup=markups.create(markup)
    )

