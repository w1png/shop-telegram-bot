from aiogram import types
import models
import constants
from markups import markups
import asyncio


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    item = models.items.Item(data["iid"])
    item_text, category, image_id, cart_dict = await asyncio.gather(
        item.format_text(constants.config["info"]["item_template"], constants.config["settings"]["currency"]),
        item.category,
        item.image_id,
        user.cart.items.dict,
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

    del_data = ',"del":"1"'
    markup = markups.create([
        cart_buttons,
        (constants.language.back, f'{{"r":"user","cid":"{category.id}"{del_data if image_id else ""}}}category'),
    ])

    if image_id:
        await callback_query.message.delete()
        return await callback_query.message.answer_photo(
            photo=image_id,
            caption=item_text,
            reply_markup=markup
        )
    return await callback_query.message.edit_text(
        text=item_text,
        reply_markup=markup
    )

