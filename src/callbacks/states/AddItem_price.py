from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import states

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    if not message.text.isdigit():
        await message.answer(constants.language.price_must_be_number)
        return

    await state.update_data(price=float(message.text))
    await message.answer(
        text=constants.language.send_item_images,
        reply_markup=markups.create([
            (constants.language.skip, f'{{"r":"admin","d":"items"}}skip')
        ])
    )

    await states.AddItem.images.set()

