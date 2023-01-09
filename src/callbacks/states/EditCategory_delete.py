from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    call = callback_query.data[callback_query.data.index("}")+1:]

    state_data = await state.get_data()

    markup = markups.create([
        (constants.language.back, f'{{"r":"admin","d":"editCategories"}}cancel')
    ])

    if call != "deleteCategory":
        await state.finish()
        return await callback_query.message.answer(
            text=constants.language.unknown_error,
            reply_markup=markup
        )


    category = models.categories.Category(state_data["category_id"])
    await category.delete()

    await callback_query.message.edit_text(
        text=constants.language.category_deleted,
        reply_markup=markup
    )


