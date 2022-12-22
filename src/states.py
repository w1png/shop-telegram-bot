from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class AddCategory(StatesGroup):
    name = State()
    parent_category = State()

