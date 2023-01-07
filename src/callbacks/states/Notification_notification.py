from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import states

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    
    await state.update_data(notification=message.text)
    await message.answer(
        text=constants.language.confirm_notification(message.text),
        reply_markup=markups.create([(
            (constants.language.yes, f'{{"r":"admin","d":"users"}}confirm'),
            (constants.language.no, f'{{"r":"admin","d":"users"}}cancel')
        )])
    )

    await states.Notification.confirmation.set()


