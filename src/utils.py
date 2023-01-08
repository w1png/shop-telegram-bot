from aiogram import types
import constants
import datetime
import json
import database

async def sendNoPermission(message: types.Message) -> None:
    await message.answer(
        text=constants.language.no_permission,
    )

