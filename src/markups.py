from aiogram import types
from typing import Any, NewType

from constants import language, JSON_ADMIN, JSON_MANAGER, JSON_USER

class Markups:
    def singleButton(self, button: types.InlineKeyboardButton) -> types.InlineKeyboardMarkup:
        return types.InlineKeyboardMarkup().add(button)

    def create(self, values: list[tuple[str, str] | tuple[tuple[str, str]]]) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup()
        for item in values:
            if isinstance(item[0], tuple):
                markup.add(*[types.InlineKeyboardButton(text=subitem[0], callback_data=subitem[1]) for subitem in item])
                continue
            markup.add(types.InlineKeyboardButton(text=item[0], callback_data=item[1]))
        return markup

    @property
    def main(self) -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(language.catalogue))
        markup.add(types.KeyboardButton(language.cart))
        markup.add(types.KeyboardButton(language.profile), types.KeyboardButton(language.faq))
        return markup

    def catalogue(self, category_list: list["Category"]) -> types.InlineKeyboardMarkup:
        return self.create([(category.name, f'{{"role": "user", "category_id": {category.id}}}category') for category in category_list])

    @property
    def faq(self) -> types.InlineKeyboardMarkup:
        return self.create([
            (language.contacts, f"{JSON_USER}contacts"),
            (language.refund_policy, f"{JSON_USER}refund_policy")
        ])

    @property
    def profile(self) -> types.InlineKeyboardMarkup:
        pass 

    @property
    def cart(self) -> types.InlineKeyboardMarkup:
        pass

    @property
    def adminPanel(self) -> types.InlineKeyboardMarkup:
        return self.create([
            (language.item_management, f"{JSON_ADMIN}item_management"),
            (language.user_management, f"{JSON_ADMIN}user_management"),
            (language.stats, f"{JSON_ADMIN}stats"),
            (language.settings, f"{JSON_ADMIN}settings")
        ])

    @property
    def orders(self) -> types.InlineKeyboardMarkup:
        pass


markups = Markups()

