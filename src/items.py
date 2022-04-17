from typing import Any
from io import BufferedReader 

from main import conn, c
from categories import Category

class Item:
    def __init__(self, id: int) -> None:
        self.id = id

    def __str__(self) -> str:
        return f"[{self.id}] {self.name}"

    def __eq__(self, item: 'Item') -> bool:
        return  self.id == item.id 

    def __del__(self):
        c.execute("DELETE FROM items WHERE id=?", [self.id])
        conn.commit()

    @property
    def _db_query(self) -> list[Any]:
         return list(c.execute("SELECT * FROM items WHERE id=?", [self.id]))[0]

    def _db_update(self, param: str, value: Any) -> None:
        c.execute(f"UPDATE items SET {param}=? WHERE id=?", [value, self.id]) 
        conn.commit()

    @property
    def name(self) -> str:
        return self._db_query[1] 
    @name.setter
    def name(self, value: str) -> None:
        self._db_update("name", value) 

    @property
    def price(self) -> float:
       return self._db_query[2] 
    @price.setter
    def price(self, value: float) -> None:
        self._db_update("price", value)

    @property
    def category(self) -> Category:
        return Category(self._db_query[3])
    @category.setter
    def category(self, value: Category | int) -> None:
        if isinstance(value, Category):
            return self._db_update("category_id", value.id)
        self._db_update("category_id", value)

    @property
    def description(self) -> str:
       return self._db_query[4] 
    @description.setter
    def description(self, value: str) -> None:
        self._db_update("description", value)

    @property
    def is_active(self) -> bool:
        return self._db_query[5] == 1
    @is_active.setter
    def is_active(self, value: bool) -> None:
        self._db_update("is_active", 1 if value else 0)

    @property
    def amount(self) -> int:
        return self._db_query[6]
    @amount.setter
    def amount(self, value: int) -> None:
        self._db_update("amount", value)

    @property
    def is_custom(self) -> bool:
       return self._db_query[7] 
    @is_custom.setter
    def is_custom(self, value: bool) -> None:
        self._db_update("is_custom", 1 if value else 0)
    
    @property
    def image(self) -> "Image":
        return self.__Image(self)

    class __Image:
        def __init__(self, item: "Item") -> None:
           self.__item = item 

        def __repr__(self) -> str:
            return self.filename

        @property
        def filename(self) -> str:
            return self.__item._db_query[8] 
        @filename.setter
        def filename(self, value: str | None) -> None:
            self.__item._db_update("image_filename", value)

        @property
        def bytes(self) -> BufferedReader:
            return open(f"images/items/{self.filename}.png", "rb")

