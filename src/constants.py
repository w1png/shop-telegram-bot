import importlib
from config import config
import os

language = importlib.import_module(f"localization.{config['settings']['language']}")

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
STATUS_DICT = {
    0: language.processing,
    1: language.delivery,
    2: language.done,
    -1: language.cancelled
}

JSON_USER = '{"role": "user"}'
JSON_MANAGER = '{"role": "manager"}'
JSON_ADMIN = '{"role": "admin"}'

