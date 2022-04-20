from aiogram import Bot

from users import User
from items import Item
from constants import language
from markups import markups

async def execute(bot: Bot, user: User, message_id: int, data: dict):
    item = Item(data["item_id"])
    text = language.item(item) + (f"\n\nВ корзине: {user.cart.items.dict[item.id]} шт." if item in user.cart.items else "")
    
    markup = markups.create([
        (language.add_to_cart, f'{{"role": "user", "item_id": {item.id}}}addToCart') if item.amount > 0 else (language.not_in_stock, 'None'),
        (language.back, f'{{"role": "user", "category_id": {item.category_id}}}category')
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

