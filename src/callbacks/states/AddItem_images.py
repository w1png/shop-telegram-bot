from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import states

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    call = callback_query.data[callback_query.data.index("}")+1:]

    if call == "skip":
        await state.update_data(images=[])
    else:
        # TODO: Add image to images
        await state.update_data()

    data = await state.get_data()

    await callback_query.message.edit_text(
        text=constants.language.format_confirm_item(data['name'], data['description'], data['category'], data['price'], data['images']),
        reply_markup=markups.create([
            ((constants.language.yes, f'{constants.JSON_ADMIN}confirm'), (constants.language.no, f'{{"r":"admin","d":"items"}}cancel'))
        ])
    )
    
    await states.AddItem.confirmation.set()


