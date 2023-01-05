from aiogram import types
import models
import constants
from markups import markups
import asyncio


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    item = models.items.Item(data["iid"])
    item_text, category, cart_dict = await asyncio.gather(
        item.format_text(constants.config["info"]["item_template"], constants.config["settings"]["currency"]),
        item.category,
        user.cart.items.dict
    )

    def cart_callback(state: int):
        return f'{{"r":"user","iid":{item.id},"s":{state},"d":"item"}}changeCart'


    item_id = str(item.id)

    if item_id in cart_dict:
        cart_buttons = (
            (constants.language.minus, cart_callback(0)),
            (cart_dict[item_id], f'None'),
            (constants.language.plus, cart_callback(1)),
        )
    else:
        cart_buttons = (constants.language.add_to_cart, cart_callback(1))

    markup = markups.create([
        cart_buttons,
        (constants.language.back, f'{{"r":"user","cid":"{category.id}"}}category'),
    ])

    return await callback_query.message.edit_text(
        text=item_text,
        reply_markup=markup
    )

