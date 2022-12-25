from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    call = callback_query.data[callback_query.data.index("}")+1:]
    print(call)

    match call:
        case "skip":
            await state.update_data(parent_category=0)
        case "parent_category":
            await state.update_data(parent_category=data["cid"])

    state_data = await state.get_data()
    print(state_data)
    await models.categories.create(state_data["name"], state_data["parent_category"])
    await callback_query.message.edit_text(
        text=constants.language.category_created,
        reply_markup=markups.create([
            (constants.language.back, f'{constants.JSON_ADMIN}categories'),
        ])
    )
    await state.finish()


