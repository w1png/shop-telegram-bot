from aiogram import types
import constants
from markups import markups

async def sendNoPermission(message: types.Message) -> None:
    await message.answer(
        text=constants.language.no_permission,
    )

async def sendStateNotFound(message: types.Message) -> None:
    await message.answer(
        text=constants.language.unknown_call_stop_state,
        reply_markup=markups.create([(constants.language.back, f"{constants.JSON_ADMIN}cancel")])
    )
