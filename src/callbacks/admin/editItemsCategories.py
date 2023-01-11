from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    await callback_query.message.edit_text(
        text=constants.language.choose_category,
        reply_markup=markups.create([
            *[
                (await category.name, f'{{"r":"admin","cid":"{category.id}"}}editItemsCategory')
                for category in await models.categories.get_categories()
            ],
            (constants.language.back, f"{constants.JSON_ADMIN}items")
        ])
    )


