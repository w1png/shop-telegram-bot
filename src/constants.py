import sqlite3
import importlib
# from config import Config

conn = sqlite3.connect("data.db")
c = conn.cursor()
language = importlib.import_module(f"localization.ru")

# Constants
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
STATUS_DICT = {
    0: language.processing,
    1: language.delivery,
    2: language.done,
    -1: language.cancelled
}

