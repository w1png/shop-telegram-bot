from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    state_data = await state.get_data()

    print(state_data)

    await models.items.create(
        name=state_data['name'],
        description=state_data['description'],
        category_id=state_data['category'],
        price=state_data['price'],
        image_id=state_data['image_id'],
    )

    text = constants.language.item_added
    markup = markups.create([
        (constants.language.back, f"{constants.JSON_ADMIN}items")
    ])

    await state.finish()

    if state_data["image_id"]:
        await callback_query.message.delete()
        return await callback_query.message.answer(
            text=text,
            reply_markup=markup
        )

    await callback_query.message.edit_text(
        text=text,
        reply_markup=markup
    )


