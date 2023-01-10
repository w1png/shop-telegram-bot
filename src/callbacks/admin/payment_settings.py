from aiogram import types
import models
import constants
from markups import markups

async def execute(callback_query: types.CallbackQuery, user: models.users.User, data: dict, message=None) -> None:
    await callback_query.message.edit_text(
        text=constants.language.payment_settings,
        reply_markup=markups.create([
           *[
                (
                    f"{constants.language.tick if payment_method['enabled'] else constants.language.cross}{payment_method['title']}",
                    f'{{"r":"admin","pmid":"{payment_method.id}"}}toggle_payment_method'
                )
                for payment_method in models.payment_methods.get_all_payment_methods()
            ],
            (constants.language.back, f"{constants.JSON_ADMIN}settings")
            

        ])
    )


