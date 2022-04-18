from typing import Any, NewType, Dict

from datetime import datetime
from random import randint

from constants import conn, c, TIME_FORMAT, STATUS_DICT
from users import User
from items import Item


class Order:
    def __init__(self, id: int) -> None:
        self.id = id

    def __repr__(self) -> str:
        return str(self.id)

    @property
    def _db_query(self) -> list[Any]:
       return list(c.execute("SELECT * FROM orders WHERE id=?", [self.id]))[0] 

    def _db_update(self, param: str, value: Any) -> None:
        c.execute(f"UPDATE orders SET {param}=? WHERE id=?", [value, self.id])
        conn.commit()

    @property
    def user(self) -> User:
        return User(self._db_query[1])

    Items = NewType("Items")
    @property
    def items(self) -> Items:
        return self.__Items(self)

    class __Items:
        def __init__(self, order: 'Order'):
            self.__order = order 

        def __repr__(self) -> list[Item]:
            return self.__items

        def __str__(self) -> str:
            return self.__raw_items

        @property
        def __raw_items(self) -> str:
            return self.__order._db_query[2]

        @property
        def __items(self) -> list[Item]:
            return list(map(lambda item: Item(int(item[0])), self.__raw_items.split(","))) 

        @property
        def price(self) -> float:
            return sum(map(lambda item: item.price, self.__items)) 

        @property
        def dict(self) -> Dict[int, int]:
            items = self.__items
            return {item.id: items.count(item) for item in set(items)}

    @property
    def phone(self) -> str:
        return self._db_query[3] 

    @property
    def email(self) -> str:
        return self._db_query[4]

    @property
    def adress(self) -> str:
        return self._db_query[5]

    @property
    def message(self) -> str:
        return self._db_query[6]

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._db_query[7], TIME_FORMAT) 

    @property
    def status(self) -> int:
         return self._db_query[8]
    @status.setter
    def status(self, value: int) -> None:
        if not value in STATUS_DICT: raise(ValueError) 
        self._db_update("status", value)


def order_list() -> list[Order]:
    return list(map(lambda order: Order(order[0]), c.execute("SELECT * FROM orders"))) 


def does_order_exist(id) -> bool:
   return len(list(c.execute("SELECT * FROM orders WHERE id=?", [id]))) == 1 


def create(user_id: int, item_list: list[Item], email: str, message=None, phone=None, adress=None) -> None:
    id = randint(100000, 999999)
    while does_order_exist(id):
        id = randint(100000, 999999)
    item_text = ",".join(map(lambda item: str(item.id), item_list))
    date = datetime.now().strftime(TIME_FORMAT) 

    c.execute(f"INSERT INTO orders VALUES ({id}, ?, ?, )", [user_id, item_text, phone, email, adress, message, date, 0])
    conn.commit()

