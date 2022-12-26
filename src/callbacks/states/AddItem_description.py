from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import states

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    await state.update_data(description=message.text)

    markup = [
        (f"[{category.id}] {await category.name}", f'{{"r":"admin","cid":{category.id}}}add_item_category')
        for category in await models.categories.get_categories()
    ]
    markup.append((constants.language.back, f'{{"r":"admin","d":"items"}}cancel'))

    await message.answer(
        text=constants.language.select_item_category,
        reply_markup=markups.create(markup)
    )

    await states.AddItem.category.set()

