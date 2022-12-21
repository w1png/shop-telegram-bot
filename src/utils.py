from aiogram import types
import constants
import datetime
import json
import database

async def sendNoPermission(message: types.Message) -> None:
    await message.answer(
        text=constants.language.no_permission,
    )

async def does_exist(user_id: int) -> bool:
    return bool(await database.fetch("SELECT id FROM users WHERE id = ?", user_id))

async def create(user_id: int) -> None:
    await database.fetch("""INSERT INTO users (
        id,
        is_admin,
        is_manager,
        notification,
        date_created,
        cart
        ) VALUES (?, 0, 0, 1, ?, ?)""",
        user_id,
        datetime.datetime.now().strftime(constants.TIME_FORMAT),
        json.dumps({
            "items": {},
            "delivery": 0,
            "payment": 0
        })
    )

async def create_if_not_exist(user_id: int) -> None:
    if not await does_exist(user_id):
        await create(user_id)

