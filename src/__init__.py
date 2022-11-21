import asyncio
from os import environ, listdir
import importlib
from json import loads
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from constants import *
from config import config
from markups import markups
import models.users as users
import items
import orders
import categories
import utils

# First startup
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, is_admin INTEGER, is_manager INTEGER, registration_date TEXT, cart TEXT, cart_delivery INTEGER, notifications INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, price REAL, category_id INTEGER, description TEXT, is_active INTEGER, amount INTEGER, is_custom INTEGER, image_filename TEXT, is_image_hidden INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, name TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER, user_id INTEGER, items TEXT, phone TEXT, email TEXT, adress TEXT, message TEXT, date TEXT, status INTEGER)")

storage = MemoryStorage()
bot = Bot(token=environ["TOKEN"])
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
    text = language.unknown_command
    markup = types.InlineKeyboardMarkup()

    match message.text:
        case language.catalogue:
            markup = markups.catalogue(categories.cat_list())
        case language.cart:
            markup = markups.cart
        case language.profile:
            markup = markups.profile
        case language.faq:
            markup = markups.faq
        case language.admin_panel:
            if not user.is_admin:
                return await utils.sendNoPermission(bot, user.id)
            markup = markups.adminPanel
        case language.orders:
            if not user.is_manager and not user.is_admin:
                return await utils.sendNoPermission(bot, user.id)
            markup = markups.orders
    
    text = text if markup == types.InlineKeyboardMarkup() else message.text
    await bot.send_message(
        chat_id=user.id,
        text=text,
        reply_markup=markup,
    )
    

# A call sends json data at the start i.e. '{"role":admin,"item_id":10}deleteItem'
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
    executor.start_polling(dp, skip_updates=True)

