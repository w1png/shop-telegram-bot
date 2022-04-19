from aiogram import types
from typing import Any, NewType

from constants import language

class Markups:
    def singleButton(self, button: types.InlineKeyboardButton) -> types.InlineKeyboardMarkup:
        return types.InlineKeyboardMarkup().add(button)

    @property
    def main(self) -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(language.catalogue))
        markup.add(types.KeyboardButton(language.cart))
        markup.add(types.KeyboardButton(language.profile), types.KeyboardButton(language.faq))
        return markup

    @property
    def categories(self) -> types.InlineKeyboardMarkup:
        pass

    @property
    def adminPanel(self) -> types.InlineKeyboardMarkup:
        pass

markups = Markups()

