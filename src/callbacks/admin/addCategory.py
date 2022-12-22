from aiogram import types
import models
import constants
from markups import markups
import states


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    if len(await models.categories.get_categories()) > 30:
        await callback_query.message.answer(constants.language.too_many_categories)
        return

    await callback_query.message.edit_text(
        text=constants.language.input_category_name,
        reply_markup=markups.create([
            (constants.language.back, '{"r":"admin","d":"categories"}cancel')
        ])
    )
    await states.AddCategory.name.set()


