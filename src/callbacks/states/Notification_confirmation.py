from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    call = callback_query.data[callback_query.data.index("}")+1:]
    if call != "confirm":
        return await callback_query.message.edit_text(
            text=constants.language.unknown_error,
            reply_markup=markups.create([
                (constants.language.back, f'{{"r":"admin","d":"users"}}cancel')
            ])
        )

    state_data = await state.get_data()

    done_users = 0
    users = await models.users.get_users()
    for user in users:
        print(user.id)
        if await user.notification:
            try:
                await constants.bot.send_message(
                    user.id,
                    state_data["notification"]
                )
                done_users += 1
            except:
                pass

    await callback_query.message.edit_text(
        text=constants.language.notification_sent(done_users, len(users)),
        reply_markup=markups.create([
            (constants.language.back, f'{{"r":"admin","d":"users"}}cancel')
        ])
    )

    await state.finish()

