from urllib import response
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
    # Required
    name = State()
    price = State()
    cat_id = State()
    desc = State()
    confirmation = State()
    
    # Additional
    image = State()

class changeItemPrice(StatesGroup):
    state_message = State()
    item_id = State()
    price = State()

class changeItemImage(StatesGroup):
    state_message = State()
    item_id = State()
    image = State()

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


# Checkout
class checkoutCart(StatesGroup):
    # Data
    user_id = State()
    item_list_comma = State()
    order_id = State()
    
    # Required
    email = State()
    additional_message = State()
    confirmation = State()

    # Additional
    phone_number = State()
    home_adress = State()
    captcha = State()

# Main settings
class changeShopName(StatesGroup):
    state_message = State()
    name = State()
    
class changeShopGreeting(StatesGroup):
    state_message = State()
    greeting = State()
    
class changeShopRefundPolicy(StatesGroup):
    state_message = State()
    refund_policy = State()
    
class changeShopContacts(StatesGroup):
    state_message = State()
    contacts = State()
    
class changeDeliveryPrice(StatesGroup):
    state_message = State()
    price = State()

class addCustomCommand(StatesGroup):
    command = State()
    response = State()
    
    
# Misc
class search(StatesGroup):
    state_message = State()
    query = State()
