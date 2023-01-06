from aiogram import types
import models
import constants
from markups import markups
import asyncio
import states


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    category = models.categories.Category(data["cid"])
    category_name, category_parent = await asyncio.gather(category.name, category.parent)

    if category_parent:
        category_parent_id, category_parent_name = category_parent.id, await category_parent.name
    else:
        category_parent_id, category_parent_name = None, None


    text = constants.language.format_category(category.id, category_name, category_parent_id, category_parent_name)
    markup = markups.create([
        (constants.language.edit_name, f'{{"r":"admin","cid":{category.id}}}editCategoryName'),
        (constants.language.edit_parent_category, f'{{"r":"admin","cid":{category.id}}}editCategoryPC'),
        (constants.language.back, f'{{"r":"admin","d":"editCategories"}}cancel')
    ])


    if message:
        await message.answer(text=text, reply_markup=markup)
    else:
        await callback_query.message.edit_text(
            text=text,
            reply_markup=markup
        )

    await states.EditCategory.main.set()


