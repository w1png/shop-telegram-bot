from typing import Any
import database
from . import items


class Category:
    def __init__(self, id: int) -> None:
        self.id = id
    
    async def __query(self, field: str) -> Any:
        return (await database.fetch(f"SELECT {field} FROM categories WHERE id = ?", self.id))[0][0]

    async def __update(self, field: str, value: Any) -> None:
        await database.fetch(f"UPDATE categories SET {field} = ? WHERE id = ?", value, self.id)

    @property
    def database_table(self) -> str:
        return """CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES categories (id)
        )"""

    @property
    async def name(self) -> str:
        return await self.__query("name")
    async def set_name(self, value: str) -> None:
        await self.__update("name", value)

    @property
    async def parent_id(self) -> int:
        return await self.__query("parent_id")
    async def set_parent_id(self, value: int) -> None:
        await self.__update("parent_id", value)
    
    @property
    async def parent(self) -> "Category":
        return Category(await self.parent_id)
    async def set_parent(self, value: "Category") -> None:
        await self.__update("parent_id", value.id)

    @property
    async def children(self) -> list["Category"]:
        return [Category(id) for id in await database.fetch("SELECT id FROM categories WHERE parent_id = ?", self.id)]
    
    @property
    async def items(self) -> list["Item"]:
        return [items.Item(id) for id in await database.fetch("SELECT id FROM items WHERE category_id = ?", self.id)]
    

async def get_categories() -> list[Category]:
    return [Category(id) for id in await database.fetch("SELECT id FROM categories WHERE parent_id=0")]

async def create(name: str, parent_id: int = 0) -> Category:
    # TODO: category creation
    pass
