from aiogram import types
from constants import language


class Markups:
    def create(self, values: list[tuple[str, str] | tuple[tuple[str, str]]]) -> types.InlineKeyboardMarkup:
        if not isinstance(values[0], tuple) or not isinstance(values[0][0], str) and not isinstance(values[0][0], tuple):
            raise TypeError("values must be a list of tuples")

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

markups = Markups()

