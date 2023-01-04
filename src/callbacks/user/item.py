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

    item_id = str(item.id)

    if item_id in cart_dict:
        cart_buttons = (
            (constants.language.minus, f'{{"r":"user","iid":{item_id}}}removeFromCart'),
            (cart_dict[item_id], f'None'),
            (constants.language.plus, add_to_cart_callback),
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

