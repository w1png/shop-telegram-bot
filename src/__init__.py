import asyncio
import os
import importlib
import json
from aiogram import Bot, Dispatcher, executor, types
import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State

import constants
from config import config
from markups import markups
import models.users as users
import models.items as items
import models.categories as categories
import utils
import database
import dotenv
import states

# First startup
if not os.path.exists("database.db"):
    tasks = [
        database.fetch(object.database_table)
        for object in [users.User(0), items.Item(0), categories.Category(0)]
    ]
    constants.loop.run_until_complete(asyncio.gather(*tasks))


dotenv.load_dotenv(dotenv.find_dotenv())
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("No token found!")
    exit(1)


storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message) -> None:
    await utils.create_if_not_exist(message.chat.id)
    user = users.User(message.chat.id)

    markup = markups.main
    if await user.is_admin:
        markup.add(types.KeyboardButton(constants.language.admin_panel))
    if await user.is_admin or await user.is_manager:
        markup.add(types.KeyboardButton(constants.language.orders))

    if "sticker.tgs" in os.listdir("."):
        with open("sticker.tgs", "rb") as sticker:
            await bot.send_sticker(user.id, sticker)

    await bot.send_message(
        chat_id=user.id,
        text=config["info"]["greeting"],
        reply_markup=markup,
    )

@dp.message_handler()
async def handle_text(message: types.Message) -> None:
    await utils.create_if_not_exist(message.chat.id)
    user = users.User(message.chat.id)
    destination = ""
    role = "user"

    match message.text:
        case constants.language.catalogue:
            destination = "catalogue"
        case constants.language.cart:
            destination = "cart"
        case constants.language.profile:
            destination = "profile"
        case constants.language.faq:
            destination = "faq"
        case constants.language.admin_panel:
            destination = "adminPanel"
            role = "admin"
        case constants.language.orders:
            destination = "orders"
            role = "manager"

    if not destination:
        await message.answer(constants.language.unknown_command)
        return

    permission = True
    match role:
        case "admin":
            permission = await user.is_admin
        case "manager":
            permission = await user.is_manager or await user.is_admin
    if not permission:
        return await utils.sendNoPermission(message)

    await importlib.import_module(f"callbacks.{role}.{destination}").execute(None, user, None, message)

@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery) -> None:
    call = callback_query.data
    user = users.User(callback_query.message.chat.id)
    data = json.loads(call[:call.index("}")+1])
    call = call[call.index("}")+1:]
    execute_args = (callback_query, user, data)

    if config["settings"]["debug"]:
        print(f"{call} | [{user.id}] | {data}")
    if call == "None": return
    if call in ["cancel", "skip"]:
        return await importlib.import_module(f"callbacks.{data['r']}.{data['d']}").execute(*execute_args)

    permission = True
    match data["r"]:
        case "admin":
            permission = await user.is_admin
        case "manager":
            permission = await user.is_manager or await user.is_admin
    if not permission:
        return await utils.sendNoPermission(callback_query.message)

    return await importlib.import_module(f"callbacks.{data['r']}.{call}").execute(*execute_args)


# states
@dp.callback_query_handler(state="*")
async def process_callback_state(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    call = callback_query.data
    user = users.User(callback_query.message.chat.id)
    data = json.loads(call[:call.index("}")+1])
    call = call[call.index("}")+1:]
    execute_args = (callback_query, user, data)

    if config["settings"]["debug"]:
        print(f"[STATE: {await state.get_state()}] {call} | [{user.id}] | {data}")
    if call == "None": return

    if call == "cancel":
        await state.finish()
        return await importlib.import_module(f"callbacks.{data['r']}.{data['d']}").execute(*execute_args)


    def parse_state(current_state: State) -> str:
        current_state_str = str(current_state)
        return current_state_str[current_state_str.index("'")+1:-2]

    current_state = await state.get_state()

    if current_state == parse_state(states.AddCategory.parent_category):
        print("AddCategory.parent_category")
        match call:
            case "skip":
                print("skip")
                await state.update_data(parent_category=0)
            case "parent_category":
                print("parent_category")
                await state.update_data(parent_category=data["cid"])

        data = await state.get_data()
        await categories.create(data["name"], data["parent_category"])
        await callback_query.message.edit_text(
            text=constants.language.category_created,
            reply_markup=markups.create([
                (constants.language.back, f'{constants.JSON_ADMIN}categories'),
            ])
        )
        await state.finish()


@dp.message_handler(state=states.AddCategory.name)
async def add_category_name(message: types.Message, state: FSMContext) -> None:

    markup = [
        (f"[{category.id}] {await category.name}", f'{{"r":"admin","cid":"{category.id}"}}parent_category')
        for category in (await categories.get_categories())
    ]
    markup.append((constants.language.skip, '{"r":"admin","d":"categories"}skip'))

    await state.update_data(name=message.text)
    await message.answer(
        text=constants.language.set_category_parent,
        reply_markup=markups.create(markup)
    )
    await states.AddCategory.next()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, loop=constants.loop)

