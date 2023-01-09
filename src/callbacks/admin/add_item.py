from aiogram import types
import models
import constants
from markups import markups
import states


async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    if not await models.categories.get_categories():
        await callback_query.message.edit_text(
            text=constants.language.no_categories,
            reply_markup=markups.create([
                (constants.language.back, f"{constants.JSON_ADMIN}items")
            ])
        )
        return


    await callback_query.message.edit_text(
        text=constants.language.input_item_name,
        reply_markup=markups.create([
            (constants.language.back, f'{{"r":"admin","d":"items"}}cancel')
        ])
    )
    
    await states.AddItem.name.set()

