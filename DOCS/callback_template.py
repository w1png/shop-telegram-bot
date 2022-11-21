from aiogram import Bot
from models.users import User

async def execute(bot: Bot, user: User, message_id: int, data: dict):
    await bot.edit_message_text(
       chat_id=user.id,
       message_id=message_id,
       text="Text",
    ) 

