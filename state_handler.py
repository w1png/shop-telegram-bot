from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import message


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

class addCat(StatesGroup):
    catid = State()
    catname = State()


class changeCatName(StatesGroup):
    catname = State()


class addItem(StatesGroup):
    itemname = State()
    cat = State()
    price = State()
    desc = State()
    confirmation = State()
