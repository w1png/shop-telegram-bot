import asyncio
from os import environ
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import importlib

from constants import *
import markups
import users
import items
import orders
import categories
import utils

# First startup
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, is_admin INTEGER, is_manager INTEGER, registration_date TEXT, cart TEXT, cart_delivery INTEGER, notifications INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER, name TEXT, price REAL, category_id INTEGER, description TEXT, is_active INTEGER, amount INTEGER, is_custom INTEGER, image_filename TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER, name TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER, user_id INTEGER, items TEXT, phone TEXT, email TEXT, adress TEXT, message TEXT, date TEXT, status INTEGER)")

storage = MemoryStorage()
bot = Bot(token=environ["TOKEN"])
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    pass 


@dp.message_handler()
async def handle_text(message):
    pass


@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    user = users.User(callback_query.message.chat.id)

    if data.startswith("admin_"):
        if not user.is_admin:
            return await utils.sendNoPermission(bot, user.id)
        importlib.import_module(f"callbacks.admin.{data[6:]}").execute()
    elif data.startswith("manager_"):
        if not user.is_manager:
            return await utils.sendNoPermission(bot, user.id)
        importlib.import_module(f"callbacks.manager.{data[8:]}").execute()
    else:
        importlib.import_module("callbacks.user").execute()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

