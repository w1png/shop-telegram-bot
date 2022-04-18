import asyncio
from os import environ
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from constants import *
import markups
import users
import items
import orders
import categories

# First startup
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, is_admin INTEGER, is_manager INTEGER, registration_date TEXT, cart TEXT, cart_delivery INTEGER, notifications INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER, name TEXT, price REAL, category_id INTEGER, description TEXT, is_active INTEGER, amount INTEGER, is_custom INTEGER, image_filename TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER, name TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER, user_id INTEGER, items TEXT, phone TEXT, email TEXT, adress TEXT, message TEXT, date TEXT, status INTEGER)")

storage = MemoryStorage()
bot = Bot(token=environ["TOKEN"])
dp = Dispatcher(bot, storage=storage)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

