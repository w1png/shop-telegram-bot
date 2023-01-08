from aiogram.dispatcher.filters.state import State, StatesGroup

class AddCategory(StatesGroup):
    name = State()
    parent_category = State()

class EditCategory(StatesGroup):
    category_id = State()
    main = State()
    name = State()
    parent_category = State()

class AddItem(StatesGroup):
    name = State()
    description = State()
    category = State()
    price = State()
    images = State()
    confirmation = State()

class Language(StatesGroup):
    language = State()

class Greeting(StatesGroup):
    greeting = State()

class Notification(StatesGroup):
    notification = State()
    confirmation = State()


class UserProfile(StatesGroup):
    id = State()
