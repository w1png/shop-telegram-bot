from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
import states
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    markup = [
        (f"[{category.id}] {await category.name}", f'{{"r":"admin","cid":"{category.id}"}}parent_category')
        for category in (await models.categories.get_categories())
    ]
    markup.append((constants.language.skip, '{"r":"admin","d":"categories"}skip'))

    await state.update_data(name=message.text)
    await message.answer(
        text=constants.language.set_parent_category,
        reply_markup=markups.create(markup)
    )
    await states.AddCategory.next()


