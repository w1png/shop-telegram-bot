from aiogram import types
from aiogram.dispatcher import FSMContext
import models
import constants
from markups import markups
import asyncio

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, state: FSMContext, message: types.Message=None) -> None:
    if message:
        await state.finish()
        user_id = message.text
        if not user_id.isdigit():
            await message.answer(constants.language.invalid_user_id)
            return await message.answer(constants.language.input_user_id)

        user_id = int(user_id)
        if not await models.users.does_exist(user_id):
            await message.answer(constants.language.user_does_not_exist)
            return await message.answer(constants.language.input_user_id)
    else:
        user_id = data["uid"]
    edit_user = models.users.User(user_id)

    username, is_admin, is_manager, date_created = await asyncio.gather(
        edit_user.username,
        edit_user.is_admin,
        edit_user.is_manager,
        edit_user.date_created
    )

    admin_text = constants.language.remove_admin_role if is_admin else constants.language.add_admin_role
    manager_text = constants.language.remove_manager_role if is_manager else constants.language.add_manager_role

    def change_user_role_callback(role: str, state: bool) -> str:
        # nr is new role
        # s is state
        return f'{{"r":"admin","nr":"{role}","s":{str(state).lower()},"uid":"{user_id}"}}change_role'

    markup = [
        (constants.language.orders, f'{{"r":"admin","uid":"{user_id}"}}orders'),
        (admin_text, change_user_role_callback("a", not is_admin)),
        (manager_text, change_user_role_callback("m", not is_manager)),
        (constants.language.back, f'{constants.JSON_ADMIN}users')
    ]
    text = constants.language.format_user_profile(
        id=edit_user.id,
        username=username,
        registration_date=date_created,
        is_admin=is_admin,
        is_manager=is_manager
    )

    if message:
        return await message.answer(text=text, reply_markup=markups.create(markup))
    await callback_query.message.edit_text(text=text, reply_markup=markups.create(markup))

