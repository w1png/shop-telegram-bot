import asyncio
from os import listdir
import importlib
from json import loads
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from constants import *
from config import config
from markups import markups
import models.users as users
import models.items as items
import models.categories as categories
import utils
import database
import dotenv

loop = asyncio.get_event_loop()

# First startup
if not os.path.exists("database.db"):
    tasks = [
        database.execute(object.database_table)
        for object in [users.User(0), items.Item(0), categories.Category(0)]
    ]
    loop.run_until_complete(asyncio.gather(*tasks))

dotenv.load_dotenv(dotenv.find_dotenv())
TOKEN = os.getenv("TOKEN")
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message) -> None:
    user = users.User(message.chat.id)

    markup = markups.main
    if user.is_admin:
        markup.add(types.KeyboardButton(language.admin_panel))
    if user.is_admin or user.is_manager:
        markup.add(types.KeyboardButton(language.orders))

    if "sticker.tgs" in listdir("."):
        with open("sticker.tgs", "rb") as sticker:
            await bot.send_sticker(user.id, sticker)

    await bot.send_message(
        chat_id=user.id,
        text=config["info"]["greeting"],
        reply_markup=markup,
    )

@dp.message_handler()
async def handle_text(message: types.Message) -> None:
    user = users.User(message.chat.id)
    destination = ""
    role = "user"

    match message.text:
        case language.catalogue:
            destination = "catalogue"
        case language.cart:
            destination = "cart"
        case language.profile:
            destination = "profile"
        case language.faq:
            destination = "faq"
        case language.admin_panel:
            destination = "admin_panel"
            role = "admin"
        case language.orders:
            destination = "orders"
            role = "manager"

    if not destination:
        return await message.answer(language.unknown_command)

    if role == "admin" and user.is_admin or role == "manager" and user.is_manager:
        return await utils.sendNoPermission(bot, message.from_user.id)

    await importlib.import_module(f"callbacks.{role}.{destination}").execute(bot, user, message.message_id)


@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery) -> None:
    call = callback_query.data
    user = users.User(callback_query.message.chat.id)
    data = loads(call[:call.index("}")+1])
    call = call[call.index("}")+1:]
    execute_args = (bot, user, callback_query.message.message_id, data)

    if config["settings"]["debug"]:
        print(f"{call} | [{user.id}] | {data}")
    if call == "None": return

    if data["role"] == "admin" and not user.is_admin:
        return await utils.sendNoPermission(bot, user.id)
    elif data["role"] == "manager" and (not user.is_admin or not user.is_manager):
        return await utils.sendNoPermission(bot, user.id)

    return await importlib.import_module(f"callbacks.{data['role']}.{call}").execute(*execute_args)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, loop=loop)

