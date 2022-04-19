from aiogram import types
from typing import Any, NewType

from constants import language

JSON_USER = '{"role": "user"}'
JSON_MANAGER = '{"role": "manager"}'
JSON_ADMIN = '{"role": "admin"}'


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

    def catalogue(self, category_list: list["Category"]) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        for category in category_list:
            markup.add(types.InlineKeyboardButton(text=category.name, callback_data=f'{{"role": "user", "category_id": {category.id}}}category'))
        return markup

    @property
    def faq(self) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text=language.contacts, callback_data=f"{JSON_USER}contacts"))
        markup.add(types.InlineKeyboardButton(text=language.refund_policy, callback_data=f"{JSON_USER}refund_policy"))
        return markup

    @property
    def profile(self) -> types.InlineKeyboardMarkup:
        pass

    @property
    def cart(self) -> types.InlineKeyboardMarkup:
        pass

    @property
    def adminPanel(self) -> types.InlineKeyboardMarkup:
        pass

    @property
    def orders(self) -> types.InlineKeyboardMarkup:
        pass


markups = Markups()

