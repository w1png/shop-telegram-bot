import json
import database
from typing import Any
from . import items

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
            FOREIGN KEY (user_id) REFERENCES users (id)
        )"""

    @property
    async def user_id(self) -> int:
        return await self.__query("user_id")
    
    @property
    async def items_json(self) -> list:
        return json.loads(await self.__query("items"))
    @property
    async def items(self) -> list[items.Item]:
        return [items.Item(item_id) for item_id in await self.items_json]

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


async def get_orders_by_status(status: int) -> list[Order]:
    return [Order(order_id) for order_id in (await database.fetch("SELECT id FROM orders WHERE status = ?", status))]

async def create(
    user_id: int,
    items: list,
    adress: str | None = None,
    phone_number: str | None = None,
    email: str | None = None,
    comment: str | None = None,
) -> Order:
    await database.fetch("INSERT INTO orders (user_id, items, adress, phone_number, email, comment) VALUES (?, ?, ?, ?, ?, ?)", user_id, json.dumps(items), adress, phone_number, email, comment)
    return Order((await database.fetch("SELECT id FROM orders ORDER BY id DESC LIMIT 1"))[0][0])


