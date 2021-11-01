from aiogram.dispatcher.filters.state import StatesGroup, State


class changeShopName(StatesGroup):
    name = State()

class notifyAll(StatesGroup):
    message = State()

class changeShopContacts(StatesGroup):
    text = State()

class changeShopRefund(StatesGroup):
    text = State()

class changeQiwiNumber(StatesGroup):
    number = State()

class changeQiwiToken(StatesGroup):
    token = State()

class changeMainBtc(StatesGroup):
    wallet = State()
    
class changeUserBalance(StatesGroup):
    bal = State()

class seeUserProfile(StatesGroup):
    userid = State()
