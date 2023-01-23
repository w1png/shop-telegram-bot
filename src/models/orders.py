import json
import database
from typing import Any

import constants
import datetime

class Order:
    def __init__(self, id: int) -> None:
        self.id = id

    async def __query(self, field: str) -> Any:
        return (await database.fetch(f"SELECT {field} FROM orders WHERE id = ?", self.id))[0][0]

    async def __update(self, field: str, value: Any) -> None:
        await database.fetch(f"UPDATE orders SET {field} = ? WHERE id = ?", value, self.id)

    @property
    def database_table(self) -> str:
        return """CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            items TEXT NOT NULL,
            adress TEXT,
            phone_number TEXT,
            email TEXT,
            comment TEXT,
            status INTEGER NOT NULL DEFAULT 0,
            date_created TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )"""

    @property
    async def user_id(self) -> int:
        return await self.__query("user_id")
    
    

    # items is a json string
        # items: [
        #   {
        #       "id": 1,
        #       "amount": 2
        #       "title": "title",
        #       "price": 100 # price per item
        #   }
        # ]
        # payment_method_id: 1
        # delivery_id: 1
        # delivery_price: 100

    @property
    async def __items_raw(self) -> str:
        return await self.__query("items")

    @property
    async def __items_json(self) -> dict:
        return json.loads(await self.__items_raw)

    @property
    async def items(self) -> list["__Item"]:
        return [self.__Item(item) for item in await self.__items_json]

    class __Item:
        def __init__(self, item_raw: str) -> None:
            self.__item_raw = item_raw
        
        def __repr__(self) -> str:
            return self.__item_raw

        def __str__(self) -> str:
            return self.__item_raw

        @property
        def dict(self) -> dict:
            return json.loads(self.__item_raw)

        @property
        def id(self) -> int:
            return int(self.dict["id"])

        @property
        def amount(self) -> int:
            return int(self.dict["amount"])

        @property
        def title(self) -> str:
            return self.dict["title"]

        @property
        def price(self) -> int:
            return int(self.dict["price"])

    @property
    async def payment_method_id(self) -> int:
        return int((await self.__items_json)["payment_method_id"])

    @property
    async def delivery_id(self) -> int:
        return int((await self.__items_json)["delivery_id"])

    @property
    async def delivery_price(self) -> int:
        return int((await self.__items_json)["delivery_price"])

    @property
    async def adress(self) -> str | None:
        return await self.__query("adress")

    @property
    async def phone_number(self) -> str | None:
        return await self.__query("phone_number")

    @property
    async def email(self) -> str | None:
        return await self.__query("email")

    @property
    async def comment(self) -> str | None:
        return await self.__query("comment")

    @property
    async def status(self) -> int:
        return await self.__query("status")
    async def set_status(self, status: int) -> None:
        await self.__update("status", status)

    @property
    async def date_created_raw(self) -> str:
        return await self.__query("date_created")
    @property
    async def date_created(self) -> datetime.datetime:
        return datetime.datetime.strptime(await self.date_created_raw, constants.TIME_FORMAT)



async def get_orders_by_status(status: int) -> list[Order]:
    return [Order(order_id) for order_id in (await database.fetch("SELECT id FROM orders WHERE status = ?", status))]

async def create(
    user_id: int,
    items_json: str,
    date_created: datetime.datetime | None,
    adress: str | None = None,
    phone_number: str | None = None,
    email: str | None = None,
    comment: str | None = None,
) -> Order:
    await database.fetch("INSERT INTO orders (user_id, items, adress, phone_number, email, comment, date_created) VALUES (?, ?, ?, ?, ?, ?)", user_id, items_json, adress, phone_number, email, comment, date_created)
    return Order((await database.fetch("SELECT id FROM orders ORDER BY id DESC LIMIT 1"))[0][0])


