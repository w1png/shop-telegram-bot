import json
from typing import Any
import database
from .import categories

class Item:
    def __init__(self, id: int) -> None:
        self.id = id
    
    async def __query(self, field: str) -> Any:
        return (await database.fetch(f"SELECT {field} FROM items WHERE id = ?", self.id))[0][0]

    async def __update(self, field: str, value: Any) -> None:
        await database.fetch(f"UPDATE items SET {field} = ? WHERE id = ?", value, self.id)

    @property
    def database_table(self) -> str:
        return """CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            price REAL NOT NULL,
            images TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )"""

    @property
    async def name(self) -> str:
        return await self.__query("name")
    async def set_name(self, value: str) -> None:
        await self.__update("name", value)

    @property
    async def description(self) -> str:
        return await self.__query("description")
    async def set_description(self, value: str) -> None:
        await self.__update("description", value)

    @property
    async def category_id(self) -> int:
        return await self.__query("category_id")
    async def set_category_id(self, value: int) -> None:
        await self.__update("category_id", value)

    @property
    async def category(self) -> "Category":
        return categories.Category(await self.category_id)
    async def set_category(self, value: "Category") -> None:
        await self.__update("category_id", value.id)

    @property
    async def price(self) -> float:
        return await self.__query("price")
    async def set_price(self, value: float) -> None:
        await self.__update("price", value)

    @property
    async def images(self) -> "__Images":
        return self.__Images(self)

    class __Images:
        def __init__(self, item: "Item") -> None:
            self.item = item

        async def __query(self) -> str:
            return (await database.fetch(f"SELECT images FROM items WHERE id = ?", self.item.id))[0][0]

        async def __update(self, value: str) -> None:
            await database.fetch(f"UPDATE items SET images = ? WHERE id = ?", value, self.item.id)

        @property
        async def list(self) -> list[str]:
            return json.loads(await self.__query())

        async def add(self, value: str) -> None:
            await self.__update(json.dumps(await self.list + [value]))

        async def remove(self, value: str) -> None:
            await self.__update(json.dumps((await self.list).remove(value)))
        

async def create(
    name: str,
    description: str,
    category: categories.Category,
    price: float,
    images: list[str]
) -> Item:
    await database.fetch("INSERT INTO items VALUES (NULL, ?, ?, ?, ?, ?)", name, description, category.id, price, json.dumps(images))
    return Item(*(await database.fetch("SELECT id FROM items ORDER BY id DESC LIMIT 1"))[0][0])
        

