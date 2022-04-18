import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import markups
import users
import items
import orders
import categories
from config import Config

language
conn = sqlite3.connect("data.db")
c = conn.cursor()


# Constants
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
STATUS_DICT = {
    0: .processing,
    1: tt.delivery,
    2: tt.done,
    -1: tt.cancelled
}


# First startup
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, is_admin INTEGER, is_manager INTEGER, registration_date TEXT, cart TEXT, cart_delivery INTEGER, notifications INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER, name TEXT, price REAL, category_id INTEGER, description TEXT, is_active INTEGER, amount INTEGER, is_custom INTEGER, image_filename TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER, name TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER, user_id INTEGER, items TEXT, phone TEXT, email TEXT, adress TEXT, message TEXT, date TEXT, status INTEGER)")

if __name__ == "__main__":
    pass
#executor.start_polling(dp, skip_updates=True, on_startup=on_startup

