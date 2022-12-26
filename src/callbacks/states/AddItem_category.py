from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import states

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    await state.update_data(category=data['cid'])
    data = await state.get_data()

    await callback_query.message.edit_text(
        text=constants.language.input_item_price,
        reply_markup=markups.create([
            (constants.language.back, f'{{"r":"admin","d":"items"}}cancel')
        ])
    )

    await states.AddItem.price.set()


