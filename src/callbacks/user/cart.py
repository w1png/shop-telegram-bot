from aiogram import types
import models
import constants
from markups import markups
import asyncio


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    cart_items_dict = await user.cart.items.dict

    if not cart_items_dict:
        if message:
            return await message.answer(constants.language.cart_empty)
        return await callback_query.message.edit_text(constants.language.cart_empty)
        
    text = constants.language.cart
    
    def changeCart_callback(item_id: int, state: int) -> str:
        return f'{{"r":"user","iid":{item_id},"s":{state},"d":"cart"}}changeCart'

    markup = []

    for item_id, amount in cart_items_dict.items():
        item = models.items.Item(item_id)

        item_name, item_price, total_price = await asyncio.gather(
            item.name,
            item.price,
            user.cart.items.total_price
        )
        currency = constants.config["settings"]["currency"]
        markup.append((f"[{item_price}{currency}] {item_name}", f"None"))
        markup += [(
            (constants.language.minus, changeCart_callback(item_id, 0)),
            (f"[{amount}] {amount*item_price}{currency}", "None"),
            (constants.language.plus, changeCart_callback(item_id, 1))
        )]

    payment_method, delivery_id = await asyncio.gather(
        user.cart.payment_method,
        user.cart.delivery_id
    )
    changePaymentMethod_callback = f"{constants.JSON_USER}changePaymentMethod"
    markup.append(
        (constants.language.payment_method, changePaymentMethod_callback) 
        if not payment_method.id else
        (payment_method["title"], changePaymentMethod_callback)
    )
    markup.append((
        constants.language.delivery if delivery_id else constants.language.self_pickup,
        f"{constants.JSON_USER}changeDelivery"
    ))
    markup.append(
        (constants.language.cart_total_price(total_price), "None")
    )
    markup.append(
        (constants.language.cart_checkout, f"{constants.JSON_USER}checkout")
    )

    markup = markups.create(markup)

    if not message:
        return await callback_query.message.edit_text(
            text=text,
            reply_markup=markup
        )
    await message.answer(
        text=text,
        reply_markup=markup
    )


