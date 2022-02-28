import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import message, user
from random import choice, randint
from string import ascii_lowercase, ascii_uppercase, digits
from captcha.image import ImageCaptcha
from re import match as matchre
from phonenumbers import parse as phoneparse
from phonenumbers import is_possible_number
from os import getcwd, listdir, remove, mkdir, rmdir, mknod
from os.path import getsize, exists
from shutil import copyfile
import datetime
import logging

import markups
import state_handler
import user as usr
import stats
import item as itm
import order as ordr
import category
import text_templates as tt
from settings import Settings
import commands 
import search

conn = sqlite3.connect("data.db")
c = conn.cursor()

logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s", filename=f"logs/{datetime.date.today().strftime('%d-%m-%Y')}.log")
settings = Settings()

storage = MemoryStorage()
bot = Bot(token=settings.get_token())
dp = Dispatcher(bot, storage=storage)

# Create a backup folder + copy the needed files there
def create_backup():
    folder_path = "backups/" + datetime.date.today().strftime("%d-%m-%Y")
    mkdir(folder_path)
    copyfile("config.ini", folder_path + "/config.ini")
    copyfile("data.db", folder_path + "/data.db")
    logging.info("backup created")
    print("Backup created!")

def clean_backups(days_ago=0):
    longest_date = datetime.date.today() - datetime.timedelta(days=days_ago)
    cleaned_size = 0
    for folder in listdir("backups"):
        if datetime.datetime.strptime(folder, "%d-%m-%Y").date() < longest_date:
            for file in listdir("backups/" + folder):
                cleaned_size += getsize(file)
                remove(file)
            rmdir("backups/" + folder)
    logging.info(f"backups cleaned ({'{:.2f}'.format(cleaned_size / 1048576)}mb)")
    return cleaned_size / 1048576

def clean_logs():
    cleaned_size = 0
    for file in listdir("logs"):
        if file == f"{datetime.date.today().strftime('%d-%m-%Y')}.log":
            continue
        cleaned_size = getsize(f"logs/{file}")
        remove(f"logs/{file}")
    logging.info(f"logs cleaned ({'{:.2f}'.format(cleaned_size / 1048576)}mb)")

    return cleaned_size / 1048576

def clean_images():
    cleaned_size = 0
    for file in listdir("images"):
        if file not in [item.get_image_id() for item in itm.get_item_list()]:
            cleaned_size = getsize(f"images/{file}")
            remove(f"images/{file}")
    logging.info(f"unused images cleaned ({'{:.2f}'.format(cleaned_size / 1048576)}mb)")
    return cleaned_size / 1048576


def get_captcha_text(): return ''.join([choice(ascii_uppercase + digits) for i in range(5)])

def generate_captcha(captcha_text):
    image = ImageCaptcha(width=280, height=90)
    image.generate(captcha_text)
    image.write(captcha_text, "images/captcha.png")
    return open("images/captcha.png", "rb")


async def notify_admins(text):
    for user in list(filter(lambda x: x.is_admin(), usr.get_user_list())):
        try:
            await bot.send_message(
                chat_id=user.get_id(),
                text=text
            )
        except:
            logging.warning(f"FAILED TO SEND TO [{user.get_id()}]")
            if settings.is_debug():
                print(f"FAILED TO SEND TO [{user.get_id()}]")


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message):
    logging.info(f"COMMAND [{message.chat.id}] {message.text}")
    if settings.is_debug():
        print(f"DEBUG: COMMAND [{message.chat.id}] {message.text}")
    user = usr.User(message.chat.id)

    markupMain = markups.get_markup_main()
    if user.is_manager() or user.is_admin():
        markupMain.row(markups.btnOrders)
    if user.is_admin():
        markupMain.row(markups.btnAdminPanel)

    try:
        if settings.is_sticker_enabled():
            if exists("sticker.tgs"):
                with open("sticker.tgs", "rb") as sti:
                    await bot.send_sticker(message.chat.id, sti)
            else:
                raise Exception
    except:
        logging.warning(f"FAILED TO SEND STICKER TO {message.chat.id}. sticker.tgs is probably missing in the bot's root folder.")
        if settings.is_debug():
            print(f"DEBUG: FAILED TO SEND STICKER TO {message.chat.id}. sticker.tgs is probably missing in the bot's root folder.")
    await bot.send_message(
        chat_id=message.chat.id,
        text=settings.get_shop_greeting(),
        reply_markup=markupMain,
    )


@dp.message_handler()
async def handle_text(message):
    logging.info(f"MESSAGE [{message.chat.id}] {message.text}")
    if settings.is_debug():
        print(f"DEBUG: MESSAGE [{message.chat.id}] {message.text}")
    user = usr.User(message.chat.id)
    
    if message.text == tt.admin_panel:
        if user.is_admin():
            await bot.send_message(
                chat_id=message.chat.id,
                text=tt.admin_panel,
                reply_markup=markups.get_markup_admin(),
            )
    elif message.text == tt.orders:
        if user.is_manager() or user.is_admin():
            await bot.send_message(
                chat_id=message.chat.id,
                text=tt.orders,
                reply_markup=markups.get_markup_orders()
            )
    elif message.text == tt.faq:
        await bot.send_message(
            chat_id=message.chat.id,
            text=tt.get_faq_template(settings.get_shop_name()),
            reply_markup=markups.get_markup_faq(),
        )
    elif message.text == tt.profile:
        await bot.send_message(
            chat_id=message.chat.id,
            text=tt.get_profile_template(user),
            reply_markup=markups.get_markup_profile(user),
        )
    elif message.text == tt.catalogue: 
        await bot.send_message(
            chat_id=message.chat.id,
            text=tt.catalogue,
            reply_markup=markups.get_markup_catalogue(category.get_cat_list()),
        )
    elif message.text == tt.cart:
        if user.get_cart():
            text = tt.cart
            markup = markups.get_markup_cart(user)
        else:
            text = tt.cart_is_empty
            markup = types.InlineKeyboardMarkup()
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=markup
        )
    elif commands.does_command_exist(command=message.text):
        await bot.send_message(
            chat_id=message.chat.id,
            text=commands.get_command_by_command(message.text).get_response()
        )
    else:
        await bot.send_message(message.chat.id, 'Не могу понять команду :(')


@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    call_data = callback_query.data
    user = usr.User(chat_id)
    
    logging.info(f"CALL [{chat_id}] {call_data}")
    if settings.is_debug():
        print(f"DEBUG: CALL [{chat_id}] {call_data}")
    
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
            try:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=tt.item_management,
                    reply_markup=markups.get_markup_itemManagement(),
                )
            except:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text=tt.item_management,
                    reply_markup=markups.get_markup_itemManagement(),
                )
        elif call_data == "addCat":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите название новой категории {tt.or_press_back}",
                reply_markup=markups.single_button(markups.btnBackItemManagement),
            )
            await state_handler.addCat.name.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data == "editCatChooseCategory":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Выберите категорию, которую хотите изменить {tt.or_press_back}",
                reply_markup=markups.get_markup_editCatChooseCategory(category.get_cat_list()),
            )
        elif call_data.startswith("editCatDelete"):
            cat = category.Category(call_data[13:])
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
            cat = category.Category(call_data[11:])
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите новое название для категории \"{cat.get_name()}\" {tt.or_press_back}",
                reply_markup=markups.single_button(markups.btnBackEditCat(cat.get_id())),
            )
            await state_handler.changeCatName.name.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(cat_id=cat.get_id())
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data.startswith("editCat"):
            cat = category.Category(call_data[7:])
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_category_data(cat),
                reply_markup=markups.get_markup_editCat(cat.get_id()),
            )
        elif call_data == "addItem":
            if not category.get_cat_list():
                await bot.edit_message_text(
                    text=f"Создайте категорию перед добавлением товара!",
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    reply_markup=markups.single_button(markups.btnBackItemManagement)
                )
            else:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=f"Введите название нового товара или нажмите на кнопку \"Назад\".",
                    reply_markup=markups.single_button(markups.btnBackItemManagement),
                )
                await state_handler.addItem.name.set()
        elif call_data == "editItemChooseCategory":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Выберите категорию товара, который вы хотите редактировать: ",
                reply_markup=markups.get_markup_editItemChooseCategory(category.get_cat_list()),
            )
        elif call_data.startswith("editItemChooseItem"):
            cat = category.Category(call_data[18:])
            text = f"Выберите товар, который вы хотите редактировать: "
            markup = markups.get_markup_editItemChooseItem(cat.get_item_list())
            try:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markup,
                )
            except:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=markup
                )

        elif call_data.startswith("editItemName"):
            item = itm.Item(call_data[12:])
            text = f"Введите новое название для \"{item.get_name()}\" {tt.or_press_back}"
            markup = markups.single_button(markups.btnBackEditItem(item.get_id()))
            
            if item.get_image_id() == "None" or not settings.is_item_image_enabled() or await item.is_hide_image():
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markup,
                )
            else:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=markup
                )

            await state_handler.changeItemName.name.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(item_id=item.get_id())
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data.startswith("editItemDesc"):
            item = itm.Item(call_data[12:])
            text = f"Введите новое описание для \"{item.get_name()}\" {tt.or_press_back}"
            markup = markups.single_button(markups.btnBackEditItem(item.get_id()))
            
            if item.get_image_id() == "None" or not settings.is_item_image_enabled():
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markup,
                )   
            else:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=markup
                )
            await state_handler.changeItemDesc.desc.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(item_id=item.get_id())
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data.startswith("editItemPrice"):
            item = itm.Item(call_data[13:])
            text = f"Введите новую цену для \"{item.get_name()}\" {tt.or_press_back}"
            markup = markups.single_button(markups.btnBackEditItem(item.get_id()))
            
            if item.get_image_id() == "None" or not settings.is_item_image_enabled() or await item.is_hide_image():
                try:
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=callback_query.message.message_id,
                        text=text,
                        reply_markup=markup,
                    )
                except:
                    await bot.delete_message(
                        chat_id=chat_id,
                        message_id=callback_query.message.message_id
                    )
                    await bot.send_message(
                        chat_id=chat_id,
                        text=text,
                        reply_markup=markup
                    )
            else:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=markup
                )

            await state_handler.changeItemPrice.price.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(item_id=item.get_id())
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data.startswith("editItemCat"):
            item = itm.Item(call_data[11:])
            text = f"Выберите новую категорию для \"{item.get_name()}\" {tt.or_press_back}"
            markup = markups.get_markup_editItemCat(item_id=item.get_id(), cat_list=category.get_cat_list())
            
            if item.get_image_id() == "None" or not settings.is_item_image_enabled():
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markup,
                )   
            else:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=markup
                )

            await state_handler.changeItemCat.cat.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(item_id=item.get_id())
        elif call_data.startswith("editItemStock"):
            item = itm.Item(call_data[13:])
            text = f"Введите новое количество товара для \"{item.get_name()}\" {tt.or_press_back}"
            markup = markups.single_button(markups.btnBackEditItem(item.get_id()))
            
            if item.get_image_id() == "None" or not settings.is_item_image_enabled():
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markup,
                )   
            else:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=markup
                )
                
            await state_handler.changeItemStock.stock.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(item_id=item.get_id())
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data.startswith("editItemHideImage"):
            item = itm.Item(call_data[17:])
            cat = category.Category(item.get_cat_id())

            try:
                item.set_hide_image(0 if await item.is_hide_image() else 1)
                text = tt.get_item_card(item) + f"\nКатегория: {cat.get_name()}"
            except:
                text = tt.error
            markup = await markups.get_markup_editItem(item)

            if item.get_image_id() == "None" or not settings.is_item_image_enabled() or await item.is_hide_image():
                try:                
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=callback_query.message.message_id,
                        text=text,
                        reply_markup=markup,
                    )
                except: # TODO: make it more compact
                    await bot.delete_message(
                        message_id=callback_query.message.message_id,
                        chat_id=chat_id
                    )
                    await bot.send_message(
                        text=text,
                        chat_id=chat_id,
                        reply_markup=markup
                    )
            else:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_photo(
                    chat_id=chat_id,
                    caption=text,
                    photo=item.get_image(),
                    reply_markup=markup
                )

        elif call_data.startswith("editItemHide"):
            item = itm.Item(call_data[12:])
            cat = category.Category(item.get_cat_id())

            try:
                item.set_active(0 if item.is_active() else 1)
                text = tt.get_item_card(item) + f"\nКатегория: {cat.get_name()}"
            except:
                text = tt.error
            markup = await markups.get_markup_editItem(item)
            
            if item.get_image_id() == "None" or not settings.is_item_image_enabled() or await item.is_hide_image():
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markup,
                )   
            else:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_photo(
                    chat_id=chat_id,
                    caption=text,
                    photo=item.get_image(),
                    reply_markup=markup
                )
                
        elif call_data.startswith("editItemDelete"):
            item = itm.Item(call_data[14:])
            cat = category.Category(item.get_cat_id())
            try:
                text = f"Товар \"{item.get_name()}\" был удалён."
                item.delete()
                markup = markups.single_button(markups.btnBackEditItemChooseItem(cat.get_id()))
            except:
                text = tt.error
                markup = markups.single_button(markups.btnBackEditItem(item.get_id()))
            
            try:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markup,
                )   
            except:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_photo(
                    chat_id=chat_id,
                    caption=text,
                    photo=item.get_image(),
                    reply_markup=markup
                )
                
        elif call_data.startswith("editItemImage"):
            item = itm.Item(call_data[13:])
            text = f"Отправьте изображение для товара {tt.or_press_back}"
            markup = markups.single_button(markups.btnBackEditItem(item.get_id()))
            
            await state_handler.changeItemImage.image.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(item_id=item.get_id())

            try:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markup,
                )
                await state.update_data(state_message=callback_query.message.message_id)
            except:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=markup
                )

        elif call_data.startswith("editItem"):
            item = itm.Item(call_data[8:])
            cat = category.Category(item.get_cat_id())
            text = tt.get_item_card(item=item) + f"\nКатегория: {cat.get_name()}"
            markup = await markups.get_markup_editItem(item)
            
            if item.get_image_id() == "None" or not settings.is_item_image_enabled() or await item.is_hide_image():
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markup,
                )   
            else:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_photo(
                    chat_id=chat_id,
                    caption=text,
                    photo=item.get_image(),
                    reply_markup=markup
                )

        # User management
        elif call_data == "userManagement":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.user_management,
                reply_markup=markups.get_markup_userManagement(),
            )
        elif call_data == "seeUserProfile":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите ID пользователя {tt.or_press_back}",
                reply_markup=markups.single_button(markups.btnBackUserManagement),
            )
            await state_handler.seeUserProfile.user_id.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data.startswith("seeUserProfile"):
            user = usr.User(int(call_data[14:]))
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_profile_template(user),
                reply_markup=markups.get_markup_seeUserProfile(user),
            )
        elif call_data.startswith("seeUserOrders"):
            edit_user = usr.User(call_data[13:])
            await bot.edit_message_text( 
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Заказы пользователя с ID {edit_user.get_id()}.",
                reply_markup=markups.get_markup_seeUserOrders(edit_user),
            )
        elif call_data.startswith("seeUserOrder"):
            order = ordr.Order(call_data[12:])
            await bot.edit_message_text(
                text=tt.get_order_template(order),
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                reply_markup=markups.get_markup_seeOrder(order, user_id=order.get_user_id())
            )
        elif call_data.startswith("changeUserManager"):
            editUser = usr.User(call_data[17:])
            editUser.set_manager(0 if editUser.is_manager() else 1)

            try:
                markupMain = markups.get_markup_main()
                if editUser.is_manager() or editUser.is_admin():
                    markupMain.row(markups.btnOrders)
                if editUser.is_admin():
                    markupMain.row(markups.btnAdminPanel)
                await bot.send_message(
                    chat_id=editUser.get_id(),
                    text=f"Ваша роль менеджера была обновлена.",
                    reply_markup=markupMain
                )
            except:
                if settings.is_debug():
                    logging.warning(f"[{user.get_id()}] FAILED TO SEND MESSAGE TO [{editUser.get_id()}]")
                    print(f"DEBUG [{user.get_id()}] FAILED TO SEND MESSAGE TO [{editUser.get_id()}]")

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_profile_template(editUser),
                reply_markup=markups.get_markup_seeUserProfile(editUser),
            )
        elif call_data.startswith("changeUserAdmin"):
            editUser = usr.User(int(call_data[15:]))
            if editUser.get_id() == user.get_id():
                markup = markups.single_button(markups.btnBackSeeUserProfile(editUser.get_id()))
                text = f"Вы не можете забрать роль администратора у себя!"
            else:
                try:
                    editUser.set_admin(0 if editUser.is_admin() else 1)
                    markup = markups.get_markup_seeUserProfile(editUser)
                    text = tt.get_profile_template(editUser)

                    try:
                        markupMain = markups.get_markup_main()
                        if editUser.is_manager() or editUser.is_admin():
                            markupMain.row(markups.btnOrders)
                        if editUser.is_admin():
                            markupMain.row(markups.btnAdminPanel)
                        await bot.send_message(
                            chat_id=editUser.get_id(),
                            text=f"Ваша роль администратора была обновлена.",
                            reply_markup=markupMain
                        )
                    except:
                        logging.warning(f"[{user.get_id()}] FAILED TO SEND MESSAGE TO [{editUser.get_id()}]")
                        if settings.is_debug():
                            print(f"DEBUG [{user.get_id()}] FAILED TO SEND MESSAGE TO [{editUser.get_id()}]")

                except:
                    text = tt.error
                    markup = markups.single_button(markups.btnBackSeeUserProfile(editUser.get_id()))
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markup,
            )
        elif call_data == "notifyEveryone":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text="Введите сообщение, которое хотите отправить ВСЕМ пользователям.",
                reply_markup=markups.single_button(markups.btnBackUserManagement),
            )
            await state_handler.notifyEveryone.message.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)

        # Stats
        elif call_data == "shopStats":
            await bot.edit_message_text(
                text=tt.shop_stats,
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                reply_markup=markups.get_markup_shopStats()
            )
        elif call_data == "registrationStats":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.registration_stats,
                reply_markup=markups.get_markup_registrationStats(),
            )
        elif call_data == "registrationStatsBack":
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text=tt.registration_stats,
                reply_markup=markups.get_markup_registrationStats(),
            )
        elif call_data.startswith("registrationStats"):
            call_data = call_data[17:]
            charts = stats.RegistrationCharts()
            
            match call_data:
                case "AllTime":
                    photo = charts.all_time()
                    text = tt.all_time
                case "Monthly":
                    photo = charts.last_x_days(30)
                    text = tt.monthly
                case "Weekly":
                    photo = charts.last_x_days(7)
                    text = tt.weekly
                case "Daily":
                    photo = charts.last_x_hours(24)
                    text = tt.daily

            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=text,
                reply_markup=markups.single_button(markups.btnBackRegistratonStats)
            )
        elif call_data == "orderStats":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.order_stats,
                reply_markup=markups.get_markup_orderStats(),
            )    
        elif call_data == "orderStatsBack":
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_message(
                chat_id=callback_query.message.chat.id,
                text=tt.order_stats,
                reply_markup=markups.get_markup_orderStats(),
            )
        elif call_data.startswith("orderStats"):
            call_data = call_data[10:]
            charts = stats.OrderCharts()
            
            match call_data:
                case "AllTime":
                    photo = charts.all_time()
                    text = tt.all_time
                case "Monthly":
                    photo = charts.last_x_days(30)
                    text = tt.monthly
                case "Weekly":
                    photo = charts.last_x_days(7)
                    text = tt.weekly
                case "Daily":
                    photo = charts.last_x_hours(24)
                    text = tt.daily

            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=text,
                reply_markup=markups.single_button(markups.btnBackOrderStats)
            )

        # Settings
        elif call_data == "shopSettings":
            await bot.edit_message_text(
                text=tt.bot_settings,
                message_id=callback_query.message.message_id,
                chat_id=chat_id,
                reply_markup=markups.get_markup_shopSettings()
            )
        elif call_data == "shopSettingsDel":
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_message(
                text=tt.bot_settings,
                chat_id=chat_id,
                reply_markup=markups.get_markup_shopSettings()
            )

        elif call_data == "mainSettings":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.main_settings,
                reply_markup=markups.get_markup_mainSettings(),
            )            
        elif call_data == "changeShopName":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите новое название магазина {tt.or_press_back}",
                reply_markup=markups.single_button(markups.btnBackMainSettings),
            )
            await state_handler.changeShopName.name.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data == "changeShopGreeting":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите новое приветствие магазина {tt.or_press_back}",
                reply_markup=markups.single_button(markups.btnBackMainSettings),
            )
            await state_handler.changeShopGreeting.greeting.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data == "changeShopRefundPolicy":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите новую политику возврата магазина {tt.or_press_back}",
                reply_markup=markups.single_button(markups.btnBackMainSettings),
            )
            await state_handler.changeShopRefundPolicy.refund_policy.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data == "changeShopContacts":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите новый текст для вкладки \"Контакты\" возврата магазина {tt.or_press_back}",
                reply_markup=markups.single_button(markups.btnBackMainSettings),
            )
            await state_handler.changeShopContacts.contacts.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)
            
        elif call_data == "itemSettings":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.item_settings,
                reply_markup=markups.get_markup_itemSettings(),
            )
            
        elif call_data == "checkoutSettings":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.checkout_settings,
                reply_markup=markups.get_markup_checkoutSettings(),
            )
        elif call_data == "changeDeliveryPrice":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите новую цену доставки {tt.or_press_back}",
                reply_markup=markups.single_button(markups.btnBackCheckoutSettings),
            )
            await state_handler.changeDeliveryPrice.price.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data.startswith("changeEnable"):
            try:
                # Checkout
                match call_data[12:]:
                    case "PhoneNumber":
                        settings.set_enable_phone_number("0" if settings.is_phone_number_enabled() else "1")
                    case "Delivery":
                        settings.set_delivery("0" if settings.is_delivery_enabled() else "1")
                    case "Captcha":
                        settings.set_enable_captcha("0" if settings.is_captcha_enabled() else "1")
                text = tt.checkout_settings
                markup = markups.get_markup_checkoutSettings()
                
                if call_data[12:] == "Sticker":
                    await bot.send_message(
                        chat_id=chat_id,
                        text=f"Для работы стикера требуется поместить sticker.tgs в корневую папку бота.",
                    )
                    settings.set_enable_sticker("0" if settings.is_sticker_enabled() else "1")
                    text = tt.main_settings
                    markup = markups.get_markup_mainSettings()
                elif call_data[12:] == "ItemImage":
                    settings.set_item_image("0" if settings.is_item_image_enabled() else "1")
                    text = tt.item_settings
                    markup = markups.get_markup_itemSettings()
                elif call_data[12:] == "Debug":
                    settings.set_debug("0" if settings.is_debug() else "1")
                    text = tt.system_settings
                    markup = markups.get_markup_systemSettings()

            except:
                text = tt.error
                if call_data[12:] in ["PhoneNumber", "Delivery", "Captcha"]:
                    markup = markups.single_button(markups.btnBackCheckoutSettings)
                elif call_data[12:] == "Sticker":
                    markup = markups.single_button(markups.btnBackMainSettings)
                elif call_data[12:] == "ItemImage":
                    markup = markups.single_button(markups.btnBackItemSettings)
                elif call_data[12:] == "Debug":
                    markup = markups.single_button(markups.btnBackSystemSettings)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markup,
            )
            
        elif call_data == "statsSettings":
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=tt.stats_settings,
                photo=stats.get_random_graph(),
                reply_markup=markups.get_markup_statsSettings()
            )
        elif call_data == "statsSettingsColor":
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=tt.graph_color,
                photo=stats.get_random_graph(),
                reply_markup=markups.get_markup_statsSettingsColor()
            )
        elif call_data.startswith("statsSettingsColor"):
            color = call_data[18:]
            match color:
                case "Black":
                    color = "000000"
                case "White":
                    color = "ffffff"
                case "Red":
                    color = "cc0000"
                case "Yellow":
                    color = "ffff00"
                case "Purple":
                    color = "a957e3"
                case "Blue":
                    color = "3299ff"
                case "Orange":
                    color = "ffa500"
                case "Green":
                    color = "4ca64c"
                case "Brown":
                    color = "4c3100"
            settings.set_barcolor(color)
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=tt.graph_color,
                photo=stats.get_random_graph(),
                reply_markup=markups.get_markup_statsSettingsColor()
            )
        elif call_data == "statsSettingsBorderWidth":
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=tt.border_width,
                photo=stats.get_random_graph(),
                reply_markup=markups.get_markup_statsSettingsBorderWidth()
            )
        elif call_data.startswith("statsSettingsBorderWidth"):
            match call_data[24:]:
                case "Default":
                    value = 1
                case "Add":
                    value = int(settings.get_borderwidth()) + 1
                case "Reduce":
                    value = int(settings.get_borderwidth()) - 1
            settings.set_borderwidth(value)
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=tt.border_width,
                photo=stats.get_random_graph(),
                reply_markup=markups.get_markup_statsSettingsBorderWidth()
            )
        elif call_data == "statsSettingsTitleFontSize":
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=tt.title_font_size,
                photo=stats.get_random_graph(),
                reply_markup=markups.get_markup_statsSettingsTitleFontSize()
            )
        elif call_data.startswith("statsSettingsTitleFontSize"):
            match call_data[26:]:
                case "Default":
                    value = 16
                case "Add":
                    value = int(settings.get_titlefontsize()) + 2
                case "Reduce":
                    value = int(settings.get_titlefontsize()) - 2
            settings.set_titlefontsize(value)
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=tt.title_font_size,
                photo=stats.get_random_graph(),
                reply_markup=markups.get_markup_statsSettingsTitleFontSize()
            )
        elif call_data == "statsSettingsAxisFontSize":
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=tt.axis_font_size,
                photo=stats.get_random_graph(),
                reply_markup=markups.get_markup_statsSettingsAxisFontSize()
            )
    
        elif call_data.startswith("statsSettingsAxisFontSize"):
            match call_data[25:]:
                case "Default":
                    value = 16
                case "Add":
                    value = int(settings.get_axisfontsize()) + 2
                case "Reduce":
                    value = int(settings.get_axisfontsize()) - 2
            settings.set_axisfontsize(value)
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=tt.axis_font_size,
                photo=stats.get_random_graph(),
                reply_markup=markups.get_markup_statsSettingsAxisFontSize()
            )
            
        elif call_data == "statsSettingsTickFontSize":
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=tt.tick_font_size,
                photo=stats.get_random_graph(),
                reply_markup=markups.get_markup_statsSettingsTickFontSize()
            )
            
        elif call_data.startswith("statsSettingsTickFontSize"):
            match call_data[25:]:
                case "Default":
                    value = 10
                case "Add":
                    value = int(settings.get_tickfontsize()) + 2
                case "Reduce":
                    value = int(settings.get_tickfontsize()) - 2
            settings.set_tickfontsize(value)
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=tt.tick_font_size,
                photo=stats.get_random_graph(),
                reply_markup=markups.get_markup_statsSettingsTickFontSize()
            )
        
        elif call_data == "additionalSettings":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.additional_settings,
                reply_markup=markups.get_markup_additionalSettings()
            )
        elif call_data == "systemSettings":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.system_settings,
                reply_markup=markups.get_markup_systemSettings()
            )
        elif call_data == "cleanImagesMenu":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.clean_images_text,
                reply_markup=markups.get_markup_cleanImagesMenu()
            )
        elif call_data == "cleanImages":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=f"Неиспользуемые фотографии были успешно удалены!\nОчищено: {'{:.1f}'.format(clean_images())}мб",
                reply_markup=markups.single_button(markups.btnBackSystemSettings)
            )
        elif call_data == "cleanLogsMenu":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.clean_logs_text,
                reply_markup=markups.get_markup_cleanLogsMenu()
            )
        elif call_data == "cleanLogs":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=f"Логи были успешно удалены!\nОчишено: {'{:.2f}'.format(clean_logs())}мб",
                reply_markup=markups.single_button(markups.btnBackSystemSettings)
            )
            
        elif call_data == "cleanDatabaseMenu":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.clean_database_text,
                reply_markup=markups.get_markup_cleanDatabaseMenu()
            )
        elif call_data == "cleanDatabase":
            settings.clean_db()
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=f"База данных была успешно очищена!",
                reply_markup=markups.single_button(markups.btnBackSystemSettings)
            )
        elif call_data == "resetSettingsMenu":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.resert_settings_text,
                reply_markup=markups.get_markup_resetSettingsMenu()
            )
        elif call_data == "resetSettings":
            settings.reset()
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=f"Настройки были успешно сброшены!",
                reply_markup=markups.single_button(markups.btnBackSystemSettings)
            )
        elif call_data == "backups":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.backups,
                reply_markup=markups.get_markup_backups()
            )
        elif call_data == "loadBackupMenu":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.load_backup,
                reply_markup=markups.get_markup_loadBackupMenu()
            )
        elif call_data.startswith("loadBackup"):
            backup_path = "backups/" + call_data[10:]
            if exists(backup_path):
                for file in listdir(backup_path):
                    try:
                        copyfile(f"{backup_path}/{file}", f"{getcwd()}/{file}")
                    except:
                        logging.error(f"Failed to copy \"{file}\" to \".\"")
                        if settings.is_debug():
                            print(f"DEBUG: Failed to copy \"{file}\" to \".\"")
                text = tt.load_backup + f"\nРезервная копия за {call_data[10:]} была успешно загружена!"
            else:
                text = f"{tt.load_backup}\n\n{tt.error} Файла {backup_path} не существует!"


            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markups.get_markup_loadBackupMenu()
            )
        elif call_data == "cleanBackupsMenu":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.clean_backups,
                reply_markup=markups.get_markup_cleanBackupsMenu()
            )
        elif call_data.startswith("cleanBackups"):
            days = 0 if call_data[12:] == "All" else int(call_data[12:])
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.clean_backups + f"\nОчищено: {'{:.2f}'.format(clean_backups(days))}мб!",
                reply_markup=markups.get_markup_cleanBackupsMenu()
            )


        # Custom commands
        elif call_data == "customCommands":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.custom_commands,
                reply_markup=markups.get_markup_customCommands()
            )
        elif call_data.startswith("deleteCommand"):
            command = commands.Command(call_data[13:])
            try:
                command.delete()
                text = tt.custom_commands
                markup = markups.get_markup_customCommands()
            except:
                text = tt.error
                markup = markups.single_button(markups.btnBackCustomCommands)
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markup
            )
        elif call_data == "addCommand":
            if len(commands.get_commands()) >= 90:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=f"Вы не можете добавить больше 90 команд!",
                    reply_markup=markups.single_button(markups.btnBackCustomCommands)
                )
            else:
                await bot.edit_message_text(
                    chat_id=callback_query.message.chat.id,
                    message_id=callback_query.message.message_id,
                    text=f"Введите новую команду {tt.or_press_back}",
                    reply_markup=markups.single_button(markups.btnBackCustomCommands)
                )
                await state_handler.addCustomCommand.command.set()
            
        # Manager tab
        elif call_data.startswith("manageOrder"):
            order = ordr.Order(call_data[11:])
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.get_order_template(order),
                reply_markup=markups.get_markup_manageOrder(order),
            )
    elif call_data.startswith("manager_") and (user.is_admin() or user.is_manager()):
        call_data = call_data[8:]

        if call_data == "orders":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.orders,
                reply_markup=markups.get_markup_orders()
            )
        elif call_data.startswith("orders"):
            match call_data[6:]:
                case "Processing":
                    order_list = ordr.get_order_list(status=0)
                    text = tt.processing
                case "Delivery":
                    order_list = ordr.get_order_list(status=1)
                    text = tt.delivery
                case "Done":
                    order_list = ordr.get_order_list(status=2)
                    text = tt.done
                case "Cancelled":
                    order_list = ordr.get_order_list(status=-1)
                    text = tt.cancelled
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markups.get_markup_ordersByOrderList(order_list)
            )
        elif call_data.startswith("seeOrder"):
            order = ordr.Order(call_data[8:])
            await bot.edit_message_text(
                text=tt.get_order_template(order),
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                reply_markup=markups.get_markup_seeOrder(order)
            )
        elif call_data.startswith("changeOrderStatusProcessing"):
            order = ordr.Order(call_data[27:])
            order.set_status(0)
            await bot.edit_message_text(
                text=tt.get_order_template(order),
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                reply_markup=markups.get_markup_seeOrder(order)
            )
        elif call_data.startswith("changeOrderStatusDelivery"):
            order = ordr.Order(call_data[25:])
            order.set_status(1)
            await bot.edit_message_text(
                text=tt.get_order_template(order),
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                reply_markup=markups.get_markup_seeOrder(order)
            )
        elif call_data.startswith("changeOrderStatusDone"):
            order = ordr.Order(call_data[21:])
            order.set_status(2)
            await bot.edit_message_text(
                text=tt.get_order_template(order),
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                reply_markup=markups.get_markup_seeOrder(order)
            )
        elif call_data.startswith("changeOrderStatusCancel"):
            order = ordr.Order(call_data[23:])
            order.set_status(-1)
            await bot.edit_message_text(
                text=tt.get_order_template(order),
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                reply_markup=markups.get_markup_seeOrder(order)
            )

    # User calls
    else:
        # FAQ
        if call_data == "faq":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_faq_template(settings.get_shop_name()),
                reply_markup=markups.get_markup_faq(),
            )
        elif call_data == "contacts":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=settings.get_shop_contacts(),
                reply_markup=markups.single_button(markups.btnBackFaq),
            )
        elif call_data == "refund":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=settings.get_refund_policy(),
                reply_markup=markups.single_button(markups.btnBackFaq),
            )

        # Profile
        elif call_data == "profile":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_profile_template(user),
                reply_markup=markups.get_markup_profile(user),
            )
        elif call_data == "myOrders":
            user = usr.User(chat_id)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.my_orders,
                reply_markup=markups.get_markup_myOrders(user.get_orders()),
            )
        elif call_data.startswith("viewMyOrder"):
            order = ordr.Order(call_data[11:])
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_order_template(order),
                reply_markup=markups.get_markup_viewMyOrder(order),
            )
        elif call_data.startswith("cancelOrder"):
            order = ordr.Order(call_data[11:])
            order.set_status(-1)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_order_template(order),
                reply_markup=markups.get_markup_viewMyOrder(order),
            )
        elif call_data.startswith("restoreOrder"):
            order = ordr.Order(call_data[12:])
            order.set_status(0)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_order_template(order),
                reply_markup=markups.get_markup_viewMyOrder(order),
            )
        elif call_data == "changeEnableNotif":
            user.set_notif_enable(0 if user.notif_on() else 1)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_profile_template(user),
                reply_markup=markups.get_markup_profile(user),
            )

        # Catalogue
        elif call_data == "catalogue":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.catalogue,
                reply_markup=markups.get_markup_catalogue(category.get_cat_list()),
            )
        elif call_data.startswith("viewCat"):
            cat = category.Category(call_data[7:])
            try:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=cat.get_name(),
                    reply_markup=markups.get_markup_viewCat(cat.get_item_list()),
                )
            except:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_message(
                    chat_id=callback_query.message.chat.id,
                    text=cat.get_name(),
                    reply_markup=markups.get_markup_viewCat(cat.get_item_list()),
                )
        elif call_data == "search":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=f"Введите поисковой запрос {tt.or_press_back}",
                reply_markup=markups.single_button(markups.btnBackCatalogue)
            )
            await state_handler.search.query.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)
        elif call_data.startswith("viewItem"):
            item = itm.Item(call_data[8:])
            text = tt.get_item_card(item=item)
            markup = markups.get_markup_viewItem(item)
            if item.get_image_id() == "None" or not settings.is_item_image_enabled() or await item.is_hide_image():
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markup,
                )   
            else:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_photo(
                    chat_id=chat_id,
                    caption=text,
                    photo=item.get_image(),
                    reply_markup=markup
                )
            
        # Cart
        elif call_data == "cart":
            if user.get_cart():
                text = tt.cart
                markup = markups.get_markup_cart(user)
            else:
                text = tt.cart_is_empty
                markup = types.InlineKeyboardMarkup()
            
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markup,
            )
        
        elif call_data == "cartDel":
            if user.get_cart():
                text = tt.cart
                markup = markups.get_markup_cart(user)
            else:
                text = tt.cart_is_empty
                markup = types.InlineKeyboardMarkup()
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=markup,
            )
        
        elif call_data == "clearCart":
            user.clear_cart()
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.cart_is_empty,
                reply_markup=types.InlineKeyboardMarkup(),
            )
        
        elif call_data.startswith("addToCartFromCart"):
            user.add_to_cart(call_data[17:])
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.cart,
                reply_markup=markups.get_markup_cart(user),
            )
        
        elif call_data.startswith("removeFromCartFromCart"):
            user.remove_from_cart(call_data[22:])
            if user.get_cart():
                text = tt.cart
                markup = markups.get_markup_cart(user)
            else:
                text = tt.cart_is_empty
                markup = types.InlineKeyboardMarkup()
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markup,
            )
        
        elif call_data.startswith("addToCart"):
            item = itm.Item(call_data[9:])
            if item.get_amount() == 0:
                text = f"Товара \"{item.get_name()}\" нет в наличии."
            else:
                user.add_to_cart(item.get_id())
                text = f"Товар \"{item.get_name()}\" был добавлен в корзину."
            if item.get_image_id() == "None" or not settings.is_item_image_enabled() or await item.is_hide_image():
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markups.single_button(markups.btnBackViewItem(item.get_id())),
                )
            else:
                await bot.delete_message(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_markup=markups.single_button(markups.btnBackViewItem(item.get_id()))
                )
                
        elif call_data == "changeCartDelivery":
            user.set_cart_delivery(0 if user.is_cart_delivery() else 1)
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.cart,
                reply_markup=markups.get_markup_cart(user),
            )
            
        elif call_data == "checkoutCart":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=f"Введите ваш Email адрес {tt.or_press_back}",
                reply_markup=markups.single_button(markups.btnBackCart),
            )
            await state_handler.checkoutCart.email.set()
            state = Dispatcher.get_current().current_state()
            await state.update_data(state_message=callback_query.message.message_id)
            await state.update_data(user_id=chat_id)
            await state.update_data(item_list_comma=user.get_cart_comma())

# State handlers
# Item management
@dp.message_handler(state=state_handler.addCat.name)
async def addCat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cat_name = message.text
    try:
        category.create_cat(cat_name)
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
    cat = category.Category(data["cat_id"])
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
        text=f"Введите цену для \"{message.text}\" {tt.or_press_back}",
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
            text=f"Выберите категорию для \"{data['name']}\" {tt.or_press_back}",
            reply_markup=markups.get_markup_addItemSetCat(category.get_cat_list()),
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
    
    if settings.is_item_image_enabled():
        text = "Отправьте изображение для товара или нажмите на кнопку \"Пропустить\"."
        markup = markups.single_button(markups.btnSkipAddItemSetImage)
        await state_handler.addItem.image.set()
    else:
        markup = markups.get_markup_addItemConfirmation()
        cat = category.Category(data["cat_id"])
        text = tt.get_item_card(name=data["name"], price=data["price"], desc=data["desc"], amount=0) + f"\nКатегория: {cat.get_name()}\n\nВы уверены, что хотите добавить \"{data['name']}\" в каталог?"    
        await state_handler.addItem.confirmation.set()
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markup,
    )

@dp.message_handler(content_types=['photo'], state=state_handler.addItem.image)
async def addItemSetImage(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    
    while True:
        image_id = "".join([choice(ascii_lowercase + digits) for _ in range(6)]) + ".png"
        if image_id not in listdir("images/"):
            break
    
    await message.photo[-1].download(destination_file=f"images/{image_id}")
    await state.update_data(image=image_id)
    
    cat = category.Category(data["cat_id"])
    text = tt.get_item_card(name=data["name"], price=data["price"], desc=data["desc"], amount=0) + f"\nКатегория: {cat.get_name()}\n\nВы уверены, что хотите добавить \"{data['name']}\" в каталог?"    
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=open(f"images/{image_id}", "rb"),
        caption=text,
        reply_markup=markups.get_markup_addItemConfirmation()
    )
    await state_handler.addItem.confirmation.set()
    
@dp.message_handler(state=state_handler.addItem.image)
async def addItemSetImageNotImage(message: types.Message, state: FSMContext):
    text = "Отправьте изображение для товара или нажмите на кнопку \"Пропустить\"."
    markup = markups.single_button(markups.btnSkipAddItemSetImage)
    await state_handler.addItem.image.set()
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markup,
    )
    await state_handler.addItem.image.set()
    

@dp.message_handler(state=state_handler.changeItemPrice.price)
async def editItemSetPrice(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    item = itm.Item(data["item_id"])
    try:
        text = f"Ценя для \"{item.get_name()}\" была изменена с {item.get_price()} на {'{:.2f}'.format(float(message.text))}."
        item.set_price(float(message.text))
    except:
        text = tt.error
    
    try:
        await bot.delete_message(
            message_id=data["state_message"],
            chat_id=message.chat.id
        )
    except:
        logging.warning(f"[{message.chat.id}] FAILED TO DELETE MESSAGE WITH ID {data['state_message']}")
        if settings.is_debug():
            print(f"DEBUG: [{message.chat.id}] FAILED TO DELETE MESSAGE WITH ID {data['state_message']}")    
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackEditItem(item.get_id())),
    )

@dp.message_handler(content_types=['photo'], state=state_handler.changeItemImage.image)
async def editItemSetImage(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    item = itm.Item(data["item_id"])

    while True:
        image_id = "".join([choice(ascii_lowercase + digits) for _ in range(6)]) + ".png"
        if image_id not in listdir("images/"):
            break
    
    try:
        await message.photo[-1].download(destination_file=f"images/{image_id}")
        item.set_image_id(image_id)
        text = f"Изображение для \"{item.get_name()}\" было обновлено."
    except:
        text = tt.error
    
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackEditItem(item.get_id()))
    )
    await state.finish()
    

@dp.message_handler(state=state_handler.changeItemImage.image)
async def editItemSetImage(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()

    await bot.send_message(
        chat_id=message.chat.id,
        text=tt.error,
        reply_markup=markups.single_button(markups.btnBackEditItem(data["item_id"]))
    )

    await state.finish()


@dp.message_handler(state=state_handler.changeItemDesc.desc)
async def editItemSetDesc(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    item = itm.Item(data["item_id"])
    try:
        text = f"Описание для \"{item.get_name()}\" было изменено с \"{item.get_desc()}\" на \"{message.text}\""
        item.set_desc(message.text)
    except:
        text = tt.error
    
    try:
        await bot.delete_message(
            message_id=data["state_message"],
            chat_id=message.chat.id
        )
    except:
        logging.warning(f"[{message.chat.id}] FAILED TO DELETE MESSAGE WITH ID {data['state_message']}")
        if settings.is_debug():
            print(f"DEBUG: [{message.chat.id}] FAILED TO DELETE MESSAGE WITH ID {data['state_message']}")       
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackEditItem(item.get_id())),
    )

@dp.message_handler(state=state_handler.changeItemName.name)
async def editItemSetName(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    item = itm.Item(data["item_id"])
    try:
        text = f"Название для \"{item.get_name()}\" было изменено на \"{message.text}\"."
        item.set_name(message.text)
    except:
        text = tt.error
    
    try:
        await bot.delete_message(
            message_id=data["state_message"],
            chat_id=message.chat.id
        )
    except:
        logging.warning(f"[{message.chat.id}] FAILED TO DELETE MESSAGE WITH ID {data['state_message']}")
        if settings.is_debug():
            print(f"DEBUG: [{message.chat.id}] FAILED TO DELETE MESSAGE WITH ID {data['state_message']}")      
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackEditItem(item.get_id())),
    )
    
@dp.message_handler(state=state_handler.changeItemStock.stock)
async def editItemStockSetStock(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    item = itm.Item(data["item_id"])
    
    try:
        if not message.text.isalnum():
            raise Exception(TypeError)
        text = f"Количество товара для \"{item.get_name()}\" было изменено с {item.get_amount()} шт. на {message.text} шт."
        item.set_amount(int(message.text))
    except:
        text = tt.error
    try:
        await bot.delete_message(
            message_id=data["state_message"],
            chat_id=message.chat.id
        )
    except:
        logging.warning(f"[{message.chat.id}] FAILED TO DELETE MESSAGE WITH ID {data['state_message']}")
        if settings.is_debug():
            print(f"DEBUG: [{message.chat.id}] FAILED TO DELETE MESSAGE WITH ID {data['state_message']}")  
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackEditItem(item.get_id())),
    )
    await state.finish()


# User management
@dp.message_handler(state=state_handler.notifyEveryone.message)
async def notifyEveryoneSetMessage(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    await state.update_data(message=message.text)
    data = await state.get_data()

    await bot.delete_message(
        message_id=data["state_message"],
        chat_id=message.chat.id
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{tt.line_separator}\n\"{message.text}\"\n{tt.line_separator}\nВы уверены, что хотите отправить данное сообщение всем пользователям?",
        reply_markup=markups.get_markup_notifyEveryoneConfirmation(),
    )
    await state_handler.notifyEveryone.confirmation.set()
    
@dp.message_handler(state=state_handler.seeUserProfile.user_id)
async def seeUserProfileSetUserID(message: types.Message, state: FSMContext):
    try:
        user_id = int(message.text)
        if usr.does_user_exist(user_id):
            user = usr.User(user_id)
            markup = markups.get_markup_seeUserProfile(user)
            text = tt.get_profile_template(user)
        else:
            text = f"Пользователя с ID {message.text} не существует." 
            markup = markups.single_button(markups.btnBackUserManagement)
    except:
        text = tt.error
        markup = markups.single_button(markups.btnBackUserManagement)
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    await bot.delete_message(
        message_id=data["state_message"],
        chat_id=message.chat.id
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markup,
    )
    await state.finish()

# Main settings
@dp.message_handler(state=state_handler.changeShopName.name)
async def changeShopNameSetName(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    try:
        text = f"Название магазина было изменено с \"{settings.get_shop_name()}\" на \"{message.text}\"."
        settings.set_shop_name(message.text)
    except:
        text = tt.error
    await bot.delete_message(
        message_id=data["state_message"],
        chat_id=message.chat.id
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackMainSettings),
    )
    await state.finish()
    
@dp.message_handler(state=state_handler.changeShopGreeting.greeting)
async def changeShopGreetingSetGreeting(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    try:
        text = f"Приветствие магазина было изменено с \"{settings.get_shop_greeting()}\" на \"{message.text}\"."
        settings.set_shop_greeting(message.text)
    except:
        text = tt.error
    await bot.delete_message(
        message_id=data["state_message"],
        chat_id=message.chat.id
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackMainSettings),
    )
    await state.finish()
    
@dp.message_handler(state=state_handler.changeShopRefundPolicy.refund_policy)
async def changeShopContactsSetContacts(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    try:
        text = f"Политика возврата магазина была изменена с \"{settings.get_shop_name()}\" на \"{message.text}\"."
        settings.set_refund_policy(message.text)
    except:
        text = tt.error
    await bot.delete_message(
        message_id=data["state_message"],
        chat_id=message.chat.id
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackMainSettings),
    )
    await state.finish()
    
@dp.message_handler(state=state_handler.changeShopContacts.contacts)
async def changeShopContactsSetContacts(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    try:
        text = f"Текст для вкладки \"Контакты\" был изменен с \"{settings.get_shop_name()}\" на \"{message.text}\"."
        settings.set_shop_contacts(message.text)
    except:
        text = tt.error
    await bot.delete_message(
        message_id=data["state_message"],
        chat_id=message.chat.id
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackMainSettings),
    )
    await state.finish()

# Checkout Settings
@dp.message_handler(state=state_handler.changeDeliveryPrice.price)
async def changeDeliveryPriceSetPrice(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    try:
        text = f"Стоимость доставки была изменена с {'{:.2f}'.format(float(settings.get_delivery_price()))}руб. на {'{:.2f}'.format(float(message.text))}руб."
        settings.set_delivery_price(float(message.text))
    except:
        text = tt.error
    await bot.delete_message(
        message_id=data["state_message"],
        chat_id=message.chat.id
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackCheckoutSettings),
    )
    await state.finish()

@dp.message_handler(state=state_handler.search.query)
async def searchSetQuery(message: types.Message, state: FSMContext):
    query = search.search_item(message.text)
    if query.match():
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Результаты поиска для \"{message.text}\":",
            reply_markup=markups.get_markup_search(query.match())
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"По вашему запросу ничего не найдено :(",
            reply_markup=markups.single_button(markups.btnBackCatalogue)
        )
    await state.finish()

# Cart checkout
# Required
@dp.message_handler(state=state_handler.checkoutCart.email)
async def checkoutCartSetEmail(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    user = usr.User(message.chat.id)
    if matchre(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", message.text): # I am not familiar with how re package works. Taken from here: https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
        await state.update_data(email=message.text)
        if settings.is_phone_number_enabled():
            text = f"Введите ваш номер телефона {tt.or_press_back}"
            await state_handler.checkoutCart.phone_number.set()
        elif settings.is_delivery_enabled() and user.is_cart_delivery():
            text = f"Введите адрес доставки {tt.or_press_back}"
            await state_handler.checkoutCart.home_adress.set()
        else:
            text = f"Введите комментарий к заказу {tt.or_press_back}"
            await state_handler.checkoutCart.additional_message.set()
    else:
        text = f"\"{message.text}\" не является действительным Email адресом."
        await state.finish()
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackCart),
    )
    
@dp.message_handler(state=state_handler.checkoutCart.phone_number)
async def checkoutCartSetPhoneNumber(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    user = usr.User(message.chat.id)
    if is_possible_number(phoneparse(message.text, "RU")):
        await state.update_data(phone_number=message.text)
        if settings.is_delivery_enabled() and user.is_cart_delivery():
            text = f"Введите адрес доставки {tt.or_press_back}"
            await state_handler.checkoutCart.home_adress.set()
        else:
            text = f"Введите комментарий к заказу {tt.or_press_back}"
            await state_handler.checkoutCart.additional_message.set()
    else:
        text = f"\"{message.text}\" не является действительным номером телефона."
        await state.finish()
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackCart),
    )
       
@dp.message_handler(state=state_handler.checkoutCart.home_adress)
async def checkoutCartSetHomeAdress(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    await state.update_data(home_adress=message.text)
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Введите комментарий к заказу {tt.or_press_back}",
        reply_markup=markups.single_button(markups.btnBackCart),
    )
    await state_handler.checkoutCart.additional_message.set()
        
@dp.message_handler(state=state_handler.checkoutCart.additional_message)
async def checkoutCartSetAdditionalMessage(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    user = usr.User(message.chat.id)
    await state.update_data(additional_message=message.text)
    if settings.is_captcha_enabled():
        captcha_text = get_captcha_text()
        await state.update_data(captcha=captcha_text)
        await bot.send_photo(
            chat_id=message.chat.id,
            caption=f"Введите текст с картинки для подтверждения заказа.",
            photo=generate_captcha(captcha_text),
            reply_markup=markups.get_markup_captcha()
        )
        await state_handler.checkoutCart.captcha.set()
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=tt.get_order_confirmation_template(item_amount_dict=user.get_cart_amount(), cart_price=user.get_cart_price(), email_adress=data["email"], additional_message=message.text, phone_number=data["phone_number"] if settings.is_phone_number_enabled() else None, home_adress=data["home_adress"] if settings.is_delivery_enabled() and user.is_cart_delivery() else None),
            reply_markup=markups.get_markup_checkoutCartConfirmation(),
        )
        await state_handler.checkoutCart.confirmation.set()
        
@dp.message_handler(state=state_handler.checkoutCart.captcha)
async def checkoutCartCheckCaptcha(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    user = usr.User(data["user_id"])
    if message.text.lower() == data["captcha"].lower():
        await bot.send_message(
            chat_id=message.chat.id,
            text=tt.get_order_confirmation_template(item_amount_dict=user.get_cart_amount(), cart_price=user.get_cart_price(), email_adress=data["email"], additional_message=data["additional_message"], phone_number=data["phone_number"] if settings.is_phone_number_enabled() else None, home_adress=data["home_adress"] if settings.is_delivery_enabled() and user.is_cart_delivery() else None),
            reply_markup=markups.get_markup_checkoutCartConfirmation(),
        )
        await state_handler.checkoutCart.confirmation.set()
    else:
        captcha_text = get_captcha_text()
        await state.update_data(captcha=captcha_text)
        await bot.send_photo(
            chat_id=message.chat.id,
            caption=f"Введите текст с картинки для подтверждения заказа.",
            photo=generate_captcha(captcha_text),
            reply_markup=markups.get_markup_captcha()
        )
        await state_handler.checkoutCart.captcha.set() 

@dp.message_handler(state=state_handler.addCustomCommand.command)
async def addCustomCommandSetCommand(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    await state.update_data(command=message.text)

    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Введите ответ для команды {tt.or_press_back}",
        reply_markup=markups.single_button(markups.btnBackCustomCommands)
    )
    await state_handler.addCustomCommand.response.set()

@dp.message_handler(state=state_handler.addCustomCommand.response)
async def addCustomCommandSetResponse(message: types.Message, state: FSMContext):
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    try:
        commands.create_command(data["command"], message.text)
        text = f"Команда \"{data['command']}\" была успешно добвалена!"
    except:
        text = tt.error
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=markups.single_button(markups.btnBackCustomCommands)
    )
    await state.finish()

# State callbacks
@dp.callback_query_handler(state='*')
async def cancelState(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    call_data = callback_query.data
    state = Dispatcher.get_current().current_state()
    data = await state.get_data()
    user = usr.User(callback_query.message.chat.id)

    logging.info(f"CALL [{chat_id}] {call_data} (STATE)")
    if settings.is_debug():
        print(f"DEBUG: CALL [{chat_id}] {call_data} (STATE)")

    if call_data[:6] == "admin_":
        call_data = call_data[6:]
        
        # Callbacks
        if call_data.startswith("addItemSetCat"):
            await state.update_data(cat_id=int(call_data[13:]))
            
            finish = False
            if len(category.Category(call_data[13:]).get_item_list()) > 85:
                text = tt.error
                finish = True
            else:
                text = f"Введите описание для \"{data['name']}\" {tt.or_press_back}"
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markups.single_button(markups.btnBackItemManagement),
            )
            if finish:
                await state.finish()
            else:
                await state_handler.addItem.desc.set()
        elif call_data == "skipSetAddItemSetImage":
            await state.update_data(image="None")
            cat = category.Category(data["cat_id"])
            text = tt.get_item_card(name=data["name"], price=data["price"], desc=data["desc"], amount=0) + f"\nКатегория: {cat.get_name()}\n\nВы уверены, что хотите добавить \"{data['name']}\" в каталог?"    
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markups.get_markup_addItemConfirmation()
            )
            await state_handler.addItem.confirmation.set()
        elif call_data == "addItemConfirm":
            try:
                itm.create_item(name=data["name"], price=data["price"], cat_id=data["cat_id"], desc=data["desc"], image_id=data["image"] if settings.is_item_image_enabled() else "None")
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
        
        elif call_data == "notifyEveryoneConfirm":
            total = len(usr.get_user_list())
            fail = 0
            for user in usr.get_user_list():
                try:
                    await bot.send_message(
                        chat_id=user.get_id(),
                        text=data["message"],
                    )
                except:
                    fail += 1

            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_message(
                chat_id=chat_id,
                text=f"Сообщение было отправлено {total - fail} из {total} пользователям.",
                reply_markup=markups.single_button(markups.btnBackUserManagement),
            )
            await state.finish()

        elif call_data.startswith("editItemSetCat"):
            item = itm.Item(data["item_id"])
            old_cat = category.Category(item.get_cat_id())
            new_cat = category.Category(call_data[14:])
            try:
                text = f"Категория для \"{item.get_name()}\" была изменена с \"{old_cat.get_name()}\" на \"{new_cat.get_name()}\"."
                item.set_cat_id(new_cat.get_id())
            except:
                text = tt.error
            
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markups.single_button(markups.btnBackEditItem(item.get_id())),
            )
            await state.finish()

        # "go-backs"
        elif call_data == "itemManagement":
            try:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=tt.item_management,
                    reply_markup=markups.get_markup_itemManagement(),
                )
            except:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_message(
                    chat_id=chat_id,
                    text=tt.item_management,
                    reply_markup=markups.get_markup_itemManagement(),
                )
            await state.finish()
        elif call_data.startswith("editCat"):
            cat = category.Category(call_data[7:])
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_category_data(cat),
                reply_markup=markups.get_markup_editCat(cat.get_id()),
            )
            await state.finish()
        elif call_data.startswith("editItem"):
            item = itm.Item(call_data[8:])
            cat = category.Category(item.get_cat_id())
            text = tt.get_item_card(item=item) + f"\nКатегория: {cat.get_name()}"
            markup = await markups.get_markup_editItem(item)
            
            if item.get_image_id() == "None" or not settings.is_item_image_enabled() and await item.is_hide_image():
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=callback_query.message.message_id,
                    text=text,
                    reply_markup=markup,
                )   
            else:
                await bot.delete_message(
                    message_id=callback_query.message.message_id,
                    chat_id=chat_id
                )
                await bot.send_photo(
                    chat_id=chat_id,
                    caption=text,
                    photo=item.get_image(),
                    reply_markup=markup
                )
            await state.finish()
        elif call_data == "userManagement":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.user_management,
                reply_markup=markups.get_markup_userManagement(),
            )
            await state.finish()
        elif call_data.startswith("seeUserProfile"):
            user = usr.User(call_data[14:])
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.get_profile_template(user),
                reply_markup=markups.get_markup_seeUserProfile(user),
            )
            await state.finish()
        elif call_data == "mainSettings":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.main_settings,
                reply_markup=markups.get_markup_mainSettings(),
            )
            await state.finish()
        elif call_data == "checkoutSettings":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.checkout_settings,
                reply_markup=markups.get_markup_checkoutSettings(),
            )
            await state.finish()
        elif call_data == "customCommands":
            await bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                text=tt.custom_commands,
                reply_markup=markups.get_markup_customCommands()
            )
            await state.finish()
        else:
            await state.finish()
    else:
        if call_data == "catalogue":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=tt.catalogue,
                reply_markup=markups.get_markup_catalogue(category.get_cat_list())
            )
            await state.finish()
        elif call_data == "cart":
            if user.get_cart():
                text = tt.cart
                markup = markups.get_markup_cart(user)
            else:
                text = tt.cart_is_empty
                markup = types.InlineKeyboardMarkup()
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=callback_query.message.message_id,
                text=text,
                reply_markup=markup,
            )
            await state.finish()
        elif call_data == "refreshCaptcha":
            captcha_text = get_captcha_text()
            await state.update_data(captcha=captcha_text)
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_photo(
                chat_id=chat_id,
                caption=f"Введите текст с картинки для подтверждения заказа.",
                photo=generate_captcha(captcha_text),
                reply_markup=markups.get_markup_captcha()
            )
            await state_handler.checkoutCart.captcha.set() 
        elif call_data == "checkoutCartConfirm":
            while True:
                order_id = randint(100000, 999999)
                if not ordr.does_order_exist(order_id):
                    break
            user_id = data["user_id"]
            item_list_comma = user.get_cart_comma()
            email = data["email"]
            additional_message = data["additional_message"]
            phone_number = data["phone_number"] if settings.is_phone_number_enabled() else None
            home_adress = data["home_adress"] if settings.is_delivery_enabled() and user.is_cart_delivery() else None
            
            try:
                order = ordr.create_order(order_id, user_id, item_list_comma, email, additional_message, phone_number=phone_number, home_adress=home_adress)
                user.clear_cart()
                text = f"Заказ с ID {order.get_order_id()} был успешно создан.\nСпасибо за заказ! Наш менеджер свяжется с вами в ближайшее время."
                for user in usr.get_notif_list():
                    try:
                        await bot.send_message(
                            chat_id=user.get_id(),
                            text=f"Новый заказ:\n{tt.get_order_template(order)}",
                            reply_markup=markups.get_markup_seeOrder(order)
                        )
                    except:
                        logging.warning(f"FAIL MESSAGE TO [{user.get_id()}]")
                        if settings.is_debug():
                            print(f"DEBUG: FAIL MESSAGE TO [{user.get_id()}]")
            except:
                text = tt.error
            await bot.delete_message(
                message_id=callback_query.message.message_id,
                chat_id=chat_id
            )
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=markups.single_button(markups.btnBackCart),
            )
            await state.finish()

async def background_runner():
    while True:
        if not exists("backups/" + datetime.date.today().strftime("%d-%m-%Y")):
            create_backup()
        await asyncio.sleep(60)

async def on_startup(dp):
    asyncio.create_task(background_runner())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
