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

    currency = constants.config["settings"]["currency_symbol"]
    total_price = 0
    for item_id, amount in cart_items_dict.items():
        item = models.items.Item(item_id)

        item_name, item_price, total_price = await asyncio.gather(
            item.name,
            item.price,
            user.cart.total_price
        )
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
    changePaymentMethod_callback = f"{constants.JSON_USER}cyclePaymentMethod"
    markup.append(
        (constants.language.payment_method, changePaymentMethod_callback) 
        if not payment_method.id else
        (payment_method["title"], changePaymentMethod_callback)
    )

    if constants.config["delivery"]["enabled"]:
        markup.append((
            constants.language.format_delivery(constants.config["delivery"]["price"]) if delivery_id else constants.language.self_pickup,
            f"{constants.JSON_USER}cycleDelivery"
        ))
    markup.append(
        (constants.language.cart_total_price(total_price, currency), "None")
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


