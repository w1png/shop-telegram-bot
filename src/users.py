from typing import Any, Dict, NewType
from aiogram.types import Message

import sqlite3
from datetime import datetime

from constants import conn, c, TIME_FORMAT
from orders import Order
from items import Item
# from config import Config


class User:
    def __init__(self, id: int) -> None:
        self.id = id

        if not does_user_exist(self.id):
            create_user(self.id)

    def __eq__(self, user: "User") -> bool:
        return self.id == user.id

    @property
    def _db_query(self) -> list[Any]:
        return list(c.execute("SELECT * FROM users WHERE id=?", [self.id]))[0]

    def _db_update(self, param: str, value: Any) -> None:
        c.execute(f"UPDATE users SET {param}=? WHERE id=?", [value, self.id])

    @property
    def is_admin(self) -> bool:
        return self._db_query[1] == 1
    @is_admin.setter
    def is_admin(self, value: bool) -> None:
        self._db_update("is_admin", 1 if value else 0)

    @property
    def is_manager(self) -> bool:
        return self._db_query[2] == 1
    @is_manager.setter
    def is_manager(self, value: bool) -> None:
        self._db_update("is_manager", 1 if value else 0)

    @property
    def notifications(self) -> bool:
        return self._db_query[3] == 1
    @notifications.setter
    def notifications(self, value: bool) -> None:
        self._db_update("notifications", 1 if value else 0)

    @property
    def registration_date(self) -> datetime:
        return datetime.strptime(self._db_query[4], TIME_FORMAT)

    @property
    def orders(self) -> list[Order]:
        return list(map(lambda order: Order(order[0]), list(c.execute("SELECT * FROM orders WHERE user_id=?", [self.id]))))
    
    Cart = NewType("Cart")
    @property
    def cart(self) -> Cart:
        return self.__Cart(self)

    class __Cart:
        def __init__(self, user: 'User') -> None:
            self._user = user

        def __repr__(self) -> list[Item]:
            return self.items

        def __str__(self) -> str:
            return self._cart_raw

        @property
        def _cart_raw(self) -> str:
            return self._user._db_query[5]

        @property
        def delivery(self) -> bool:
            return self._user._db_query[6] == 1
        @delivery.setter
        def delivery(self, value: bool) -> None:
            self._user._db_update("delivery", 1 if value else 0)

        Items = NewType("Items")
        @property
        def items(self) -> Items:
            return self.__Items(self)

        class __Items:
            def __init__(self, cart: Cart) -> None:
                self.cart = cart

            def __repr__(self) -> list[Item]:
                return self.__items

            def __str__(self) -> str:
                return self.cart.__cart_raw

            @property
            def __items(self) -> list[Item]:
                if not self.cart.__cart_raw:
                    return list()
                return list(map(Item, [item_id for item_id in self.cart._cart_raw.split(",")]))

            def add(self, item: Item) -> None:
                return self.cart._user._db_update("cart", ",".join(list(map(lambda item: str(item.id), self.__items))))

            def remove(self, item: Item) -> None:
                new_list = list(map(lambda item: str(item.id), self.__items))
                new_list.remove(str(item.id))
                return self.cart._user._db_update("cart", ','.join(new_list)) 

            def clear(self) -> None:
                return self.cart._user.db_update("cart", None)

            @property
            def price(self) -> float:
                return sum(map(lambda item: item.price, self.__items))

            @property
            def dict(self) -> Dict[int, int]:
                items = self.__items
                return {item.id: items.count(item) for item in set(items)}
        
        @property
        def price(self) -> float:
            return self.items.price + Config.delivery_price if self.delivery else 0


def create_user(id: int) -> None:
    c.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)", [id, 0, 0, datetime.now().strftime(TIME_FORMAT), None, 0])
    conn.commit()


def does_user_exist(id: int) -> bool:
   return len(list(c.execute("SELECT * FROM users WHERE id=?", [id]))) != 0


def get_user_login(message: Message) -> str:
    return message.from_user.username


def user_list():
    return list(map(lambda user: User(user[0]), list(c.execute("SELECT * FROM users"))))

