from aiogram import Bot
from constants import language

async def sendNoPermission(bot: Bot, id: int) -> None:
    await bot.send_message(
        chat_id=id,
        text=language.no_permission,
    )

