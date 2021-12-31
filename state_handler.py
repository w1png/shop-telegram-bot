from aiogram.dispatcher.filters.state import StatesGroup, State

# Item management
class addCat(StatesGroup):
    state_message = State()
    name = State()

class changeCatName(StatesGroup):
    state_message = State()
    cat_id = State()
    name = State()

class addItem(StatesGroup):
    name = State()
    price = State()
    cat_id = State()
    desc = State()
    confirmation = State()

class changeItemPrice(StatesGroup):
    state_message = State()
    item_id = State()
    price = State()

class changeItemDesc(StatesGroup):
    state_message = State()
    item_id = State()
    desc = State()

class changeItemName(StatesGroup):
    state_message = State()
    item_id = State()
    name = State()

class changeItemCat(StatesGroup):
    item_id = State()
    cat = State()
    
class changeItemStock(StatesGroup):
    item_id = State()
    state_message = State()
    stock = State()

# User management
class notifyEveryone(StatesGroup):
    state_message = State()
    message = State()
    confirmation = State()

class seeUserProfile(StatesGroup):
    state_message = State()
    user_id = State()
    
class checkoutCart(StatesGroup):
    # Data
    state_message = State()
    user_id = State()
    item_list_comma = State()
    
    # Required
    email = State()
    additional_message = State()

    # Additional
    phone_number = State()
    home_adress = State()
    captcha = State()
