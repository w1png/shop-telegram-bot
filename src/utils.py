from aiogram import types
import constants

async def sendNoPermission(message: types.Message) -> None:
    await message.answer(
        text=constants.language.no_permission,
    )

