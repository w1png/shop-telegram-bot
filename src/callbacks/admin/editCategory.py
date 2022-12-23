from aiogram import types
import models
import constants
from markups import markups
import asyncio


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    category = models.categories.Category(data["cid"])
    category_name, category_parent = await asyncio.gather(category.name, category.parent)

    if category_parent:
        category_parent_id, category_parent_name = category_parent.id, await category_parent.name
    else:
        category_parent_id, category_parent_name = None, None

    await callback_query.message.edit_text(
        text=constants.language.format_category(category.id, category_name, category_parent_id, category_parent_name),
        reply_markup=markups.create([
            (constants.language.edit_name, f'{{"r":"admin","cid":{category.id}}}editCategoryName'),
            (constants.language.edit_parent_category, f'{{"r":"admin","cid":{category.id}}}editCategoryParentCategory'),
            (constants.language.back, f"{constants.JSON_ADMIN}editCategories"),
        ])
    )


