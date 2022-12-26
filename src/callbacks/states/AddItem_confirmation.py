from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    await state.update_data()
    data = await state.get_data()

    await models.items.create(
        name=data['name'],
        description=data['description'],
        category_id=data['category'],
        price=data['price'],
        images=data['images'],
    )

    await callback_query.message.edit_text(
        text=constants.language.item_added,
        reply_markup=markups.create([
            (constants.language.back, f"{constants.JSON_ADMIN}items")
        ])
    )

    await state.finish()


