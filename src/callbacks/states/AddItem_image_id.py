from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import states

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    state_data = await state.get_data()

    def format_text(image_id: str) -> str:
        return constants.language.format_confirm_item(state_data['name'], state_data['description'], state_data['category'], state_data['price'], image_id)

    markup = markups.create([
        ((constants.language.yes, f'{constants.JSON_ADMIN}confirm'), (constants.language.no, f'{{"r":"admin","d":"items"}}cancel'))
    ])

    if message:
        if not message.photo:
            return

        file_id = message.photo[-1].file_id
        await state.update_data(image_id=file_id)
        await message.answer_photo(
            photo=file_id,
            caption=format_text(file_id),
            reply_markup=markup
        )
    else:
        call = callback_query.data[callback_query.data.index("}")+1:]

        if call == "skip":
            await state.update_data(image_id=None)
            await callback_query.message.edit_text(
                text=format_text(""),
                reply_markup=markup
            )
        else:
            return

    await states.AddItem.confirmation.set()

