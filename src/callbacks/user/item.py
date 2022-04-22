from aiogram import Bot

from users import User
from items import Item
from constants import language, JSON_USER
from markups import markups

async def execute(bot: Bot, user: User, message_id: int, data: dict):
    item = Item(data["item_id"])
    text = language.item(item)
    
    add_to_cart_callback = f'{{"role": "user", "item_id": {item.id}, "dest": "item"}}addToCart'
    cross_button = (language.cross, f'{JSON_USER}None')
    cart_button = (language.add_to_cart, add_to_cart_callback) if item.amount != 0 else (language.not_in_stock, f'{JSON_USER}None')
    if item in user.cart.items:
        item_cart_quantity = user.cart.items.dict[item.id]
        text += f"\n\nВ корзине: {user.cart.items.dict[item.id]} шт."
        cart_button  = ((
            (language.minus, f'{{"role": "user", "item_id": {item.id}, "dest": "item"}}removeFromCart') if item_cart_quantity != 0 else cross_button,
            (item_cart_quantity, f'{JSON_USER}None'),
            (language.plus, add_to_cart_callback) if item_cart_quantity < item.amount else cross_button 
        ))

    btn_back = (language.back, f'{{"role": "user", "category_id": {item.category_id}}}category')
    markup = markups.create([
        cart_button,
        btn_back
    ])


    if not item.image.is_hidden and item.image.filename:
        return await bot.send_photo(
            chat_id=user.id,
            caption=text,
            photo=item.image.bytes,
            reply_markup=markup,
        )

    await bot.edit_message_text(
       chat_id=user.id,
       message_id=message_id,
       text=text,
       reply_markup=markup,
    ) 

