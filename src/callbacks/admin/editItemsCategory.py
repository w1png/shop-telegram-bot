from aiogram import types
import models
import constants
from markups import markups


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    category = models.categories.Category(data["cid"])
    
    text = constants.language.format_editItemsCategory_text(await category.name)
    markup = markups.create([
        *[
            (f"[{item.id}] {await item.name}", f'{{"r":"admin","iid":{item.id}}}editItem')
            for item in await category.items
        ],
        (constants.language.back, f"{constants.JSON_ADMIN}editItemsCategories")
    ])

    
    try:
        await callback_query.message.edit_text(
            text=text,
            reply_markup=markup
        )
    except:
        await callback_query.message.delete()
        await callback_query.message.answer(
            text=text,
            reply_markup=markup
        )


