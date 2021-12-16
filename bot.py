import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import datetime
from random import choice, randint
from aiogram.dispatcher import FSMContext
from string import ascii_letters, digits
from aiogram.types import message, message_entity, message_id, user
from configparser import ConfigParser
from aiogram.types.callback_query import CallbackQuery

import markups
import state_handler
import user as usr
import stats
import item as itm
import text_templates as tt


conn = sqlite3.connect('data.db')
c = conn.cursor()

conf = ConfigParser()
conf.read('config.ini', encoding='utf8')

storage = MemoryStorage()
bot = Bot(token=conf['main']['token'])
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    conf = ConfigParser()
    conf.read('config.ini', encoding='utf8')
    user = usr.User(message.chat.id)

    markupMain = markups.get_markup_main()
    if user.is_admin():
        markupMain.row(markups.btnAdminPanel)
    if user.is_support():
        markupMain.row(markups.btnSupportMenu)

    if conf["shop_settings"]["enable_sticker"] == "1":
        sti = open('AnimatedSticker.tgs', 'rb')
        await bot.send_sticker(message.chat.id, sti)
        sti.close()
    await bot.send_message(
        chat_id=message.chat.id,
        text=conf["shop_settings"]["shop_greeting"],
        reply_markup=markupMain,
    )


@dp.message_handler()
async def handle_text(message):
    user = usr.User(message.chat.id)
    conf = ConfigParser()
    conf.read('config.ini', encoding='utf8')
    
    if message.text == tt.admin_panel:
        if user.is_admin():
            await bot.send_message(
                chat_id=message.chat.id,
                text=tt.admin_panel,
                reply_markup=markups.get_markup_admin(),
            )
    elif message.text == tt.faq:
        await bot.send_message(
            chat_id=message.chat.id,
            text=tt.get_faq_template(conf["shop_settings"]["shop_name"]),
            reply_markup=markups.get_markup_faq(),
        )
    elif message.text == tt.profile:
        await bot.send_message(
            chat_id=message.chat.id,
            text=tt.get_profile_template(user.get_id(), user.get_orders(), user.get_balance(), user.get_register_date()),
            reply_markup=markups.get_markup_profile(user_id=user.get_id()),
        )
    elif message.text == tt.catalogue: 
        await bot.send_message(
            chat_id=message.chat.id,
            text=tt.catalogue,
            reply_markup=markups.get_markup_catalogue(itm.get_cat_list()),
        )
    else:
        await bot.send_message(message.chat.id, 'Не могу понять команду :(')


@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    call_data = callback_query.data
    
    conf = ConfigParser()
    conf.read('config.ini', encoding='utf8')
    user = usr.User(chat_id)
    
    # Admin calls
    if call_data.startswith("admin_") and user.is_admin():
        call_data = call_data[6:]
        
        if call_data == "adminPanel":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.admin_panel,
                reply_markup=markups.get_markup_admin(),
            )

        # Admin tabs
        # Item management
        elif call_data == "itemManagement":
            await bot.edit_message_text(
                text=tt.item_management,
                message_id=callback_query.message.message_id,
                chat_id=chat_id,
                reply_markup=markups.get_markup_itemManagement()
            )
        elif call_data == "addCat":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Введите название новой категории или нажмите на кнопку \"Назад\".",
                reply_markup=markups.single_button(markups.btnBackItemManagement),
            )
            await state_handler.addCat.name.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data == "editCatChooseCategory":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Выберите категорию, которую хотите изменить или нажмите на кнопку \"Назад\".",
                reply_markup=markups.get_markup_editCatChooseCategory(itm.get_cat_list()),
            )
        elif call_data.startswith("editCatDelete"):
            cat = itm.Category(call_data[13:])
            try:
                text = f"Категория {cat.get_name()} была успешно удалена."
                cat.delete()
            except:
                text = f"Произошла ошибка!"                
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markups.single_button(markups.btnBackEditCatChooseCategory),
            )
        elif call_data.startswith("editCatName"):
            cat = itm.Category(call_data[11:])
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите новое название для категории \"{cat.get_name()}\" или нажмите на кнопку \"Назад\".",
                reply_markup=markups.single_button(markups.btnBackEditCat(cat.get_id())),
            )
            await state_handler.changeCatName.name.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(cat_id=cat.get_id())
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data.startswith("editCat"):
            cat = itm.Category(call_data[7:])
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_category_data(cat),
                reply_markup=markups.get_markup_editCat(cat.get_id()),
            )
        elif call_data == "addItem":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите название нового товара или нажмите на кнопку \"Назад\".",
                reply_markup=markups.single_button(markups.btnBackItemManagement),
            )
            await state_handler.addItem.name.set()
        elif call_data == "editItem":
            pass

        # User management
        elif call_data == "userManagement":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.user_management,
                reply_markup=markups.get_markup_userManagement(),
            )

        elif call_data == "seeUserProfile":
            pass

        elif call_data == "notifyEveryone":
            pass

        # Stats
        elif call_data == "shopStats":
            await bot.edit_message_text(
                text=tt.shop_stats,
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                reply_markup=markups.get_markup_shopStats()
            )

        elif call_data == "registrationStats":
            pass
    
        elif call_data == "orderStats":
            pass

        # Settings
        elif call_data == "shopSettings":
            await bot.edit_message_text(
                text=tt.bot_settings,
                message_id=callback_query.message.message_id,
                chat_id=chat_id,
                reply_markup=markups.get_markup_shopSettings()
            )

        elif call_data == "mainSettings":
            pass

        elif call_data == "statsSettings":
            pass
    
    # Non admin calls
    else:
        # FAQ
        if call_data == "faq":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_faq_template(conf["shop_settings"]["shop_name"]),
                reply_markup=markups.get_markup_faq(),
            )
        elif call_data == "contacts":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=conf["shop_settings"]["shop_contacts"],
                reply_markup=markups.single_button(markups.btnBackFaq),
            )
        elif call_data == "refund":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=conf["shop_settings"]["refund_policy"],
                reply_markup=markups.single_button(markups.btnBackFaq),
            )

        # Profile
        elif call_data == "profile":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_profile_template(user.get_id(), user.get_orders(), user.get_balance(), user.get_register_date()),
                reply_markup=markups.get_markup_profile(user_id=user.get_id()),
            )
        elif call_data == "myOrders":
            user = usr.User(chat_id)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.my_orders,
                reply_markup=markups.get_markup_myOrders(user.get_orders()),
            )
        elif call_data.startswith("seeMyOrder"):
            pass
        elif call_data == "mySupportTickets":
            pass
        


            


# State handlers
# Item management
@dp.message_handler(state=state_handler.addCat.name)
async def addCat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cat_name = message.text

    try:
        itm.create_cat(cat_name)
        text = tt.get_category_was_created_successfuly(cat_name)
    except:
        text = tt.error

    await bot.delete_message(
        message_id=data["state_message"],
        chat_id=message.chat.id
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackItemManagement),
    )
    await state.finish()

@dp.message_handler(state=state_handler.changeCatName.name)
async def changeCatName(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cat = itm.Category(data["cat_id"])
    cat_name = message.text

    try:
        text = f"Название категории \"{cat.get_name()}\" было изменено на \"{cat_name}\"."
        cat.set_name(cat_name)
    except:
        text = tt.error

    await bot.delete_message(
        message_id=data["state_message"],
        chat_id=message.chat.id
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackEditCat(cat.get_id())),
    )
    await state.finish()

@dp.message_handler(state=state_handler.addItem.name)
async def addItemSetName(message: types.Message, state: FSMContext):
    data = await state.get_data()
    state = Dispatcher.get_current().current_state()
    await state.update_data(name=message.text)

    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Введите цену для \"{message.text}\" или нажмите на кнопку \"Назад\".",
        reply_markup=markups.single_button(markups.btnBackItemManagement),
    )
    await state_handler.addItem.price.set()

@dp.message_handler(state=state_handler.addItem.price)
async def addItemSetPrice(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        state = Dispatcher.get_current().current_state()
        await state.update_data(price=float(message.text))
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Выберите категорию для \"{data['name']}\" или нажмите на кнопку \"Назад\".",
            reply_markup=markups.get_markup_addItemSetCat(),
        )
        await state_handler.addItem.cat_id.set()
    except:
        await bot.send_message(
            chat_id=message.chat.id,
            text=tt.error,
            reply_markup=markups.single_button(markups.btnBackItemManagement),
        )
        await state.finish()

@dp.message_handler(state=state_handler.addItem.desc)
async def addItemSetDesc(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    await state.update_data(desc=message.text)
    data = await state.get_data()
    
    cat = itm.Category(data["cat_id"])
    text = tt.get_item_card(name=data["name"], price=data["price"], desc=data["desc"]) + f"\nКатегория: {cat.get_name()}\n\nВы уверены, что хотите добавить \"{data['name']}\" в каталог?"
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.get_markup_addItemConfirmation(),
    )
    await state_handler.addItem.confirmation.set()


# State callbacks
@dp.callback_query_handler(state='*')
async def cancelState(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    call_data = callback_query.data
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()

    if call_data[:6] == "admin_":
        call_data = call_data[6:]
        
        # Callbacks
        if call_data.startswith("addItemSetCat"):
            await state.update_data(cat_id=int(call_data[13:]))
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите описание для \"{data['name']}\" или нажмите на кнопку \"Назад\".",
                reply_markup=markups.single_button(markups.btnBackItemManagement),
            )
            await state_handler.addItem.desc.set()

        elif call_data == "addItemConfirm":
            try:
                itm.create_item(data["name"], data["price"], data["cat_id"], data["desc"])
                text = f"Товар {data['name']} был создан."
            except:
                text = tt.error
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=markups.single_button(markups.btnBackItemManagement),
            )
            await state.finish()
                

        # "go-backs"
        elif call_data == "itemManagement":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.item_management,
                reply_markup=markups.get_markup_itemManagement(),
            )
        elif call_data.startswith("editCat"):
            cat = itm.Category(call_data[7:])
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_category_data(cat),
                reply_markup=markups.get_markup_editCat(cat.get_id()),
            )
        else:
            await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
