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

    add_to_cart_callback = f'{{"r":"user","iid":{item.id}}}addToCart'

    if item.id in cart_dict:
        cart_buttons = (
            (constants.language.minus, add_to_cart_callback),
            (cart_dict[item.id], f'None'),
            (constants.language.plus, f'{{"r":"user","iid":{item.id}}}removeFromCart'),
        )
    else:
        cart_buttons = (constants.language.add_to_cart, add_to_cart_callback)

    markup = markups.create([
        cart_buttons,
        (constants.language.back, f'{{"r":"user","cid":"{category.id}"}}category'),
    ])

    return await callback_query.message.edit_text(
        text=item_text,
        reply_markup=markup
    )

