from typing import Any

from main import conn, c


class Category:
    def __init__(self, id: int) -> None:
        self.id = id

    def __eq__(self, category: "Category") -> bool:
        return self.id == category.id

    def __str__(self) -> str:
        return f"[{self.id}] {self.name}"

    def __del__(self) -> None:
        c.execute("DELETE FROM categories WHERE id=?", [self.id])
        conn.commit()

    @property
    def _db_query(self) -> list[Any]:
        return list(c.execute(f"SELECT * FROM categories WHERE id=?", [self.id]))[0]

    def _db_update(self, param: str, value: Any) -> None:
        c.execute(f"UPDATE categories SET {param}=? WHERE id=?", [value, self.id])
        conn.commit()

    @property
    def name(self) -> str:
        return self._db_query[1]
    @name.setter
    def name(self, value: str) -> None:
        self._db_update("name", value)

    @property
    def items(self):
        return list(map(lambda item: Item(item[0]), c.execute(f"SELECT * FROM items WHERE category_id=?", [self.id])))


def cat_list():
    return list(map(lambda category: Category(category[0]), c.execute(f"SELECT * FROM cats")))
    

def create(name):
    c.execute(f"INSERT INTO categories(name) VALUES(?)", [name])
    conn.commit()

