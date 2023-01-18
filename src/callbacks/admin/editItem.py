from aiogram import types
import asyncio
import models
import constants
from markups import markups
import states


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    item = models.items.Item(data["iid"])

    item_image, item_category_id, text, is_hidden = await asyncio.gather(
        item.image_id,
        item.category_id,
        item.format_text(
            constants.config["info"]["item_template"],
            constants.config["settings"]["currency_symbol"]
        ),
        item.is_hidden
    )

    markup = markups.create([
        (constants.language.edit_name, f'{{"r":"admin","iid":{item.id}}}editItemName'),
        (constants.language.edit_description, f'{{"r":"admin","iid":{item.id}}}editItemDescription'),
        (constants.language.edit_price, f'{{"r":"admin","iid":{item.id}}}editItemPrice'),
        (constants.language.edit_category, f'{{"r":"admin","iid":{item.id}}}editItemCategory'),
        (constants.language.edit_image, f'{{"r":"admin","iid":{item.id}}}editItemImage'),
        (constants.language.show if is_hidden else constants.language.hide, f'{{"r":"admin","iid":{item.id}}}toggleIsHidden'),
        (constants.language.delete, f'{{"r":"admin","iid":{item.id}}}deleteItem'),
        (constants.language.back, f'{{"r":"admin","cid":{item_category_id},"d":"editItemsCategory"}}cancel')
    ])

    await states.EditItem.main.set()

    if message:
        if item_image:
            await message.delete()
            await message.answer_photo(
                photo=item_image,
                caption=text,
                reply_markup=markup
            )
        else:
            await message.answer(
                text=text,
                reply_markup=markup
            )
        return

    if item_image:
        await callback_query.message.delete()
        await callback_query.message.answer_photo(
            photo=await item.image_id,
            caption=text,
            reply_markup=markup
        )
        return

    await callback_query.message.edit_text(
        text=text,
        reply_markup=markup
    )

