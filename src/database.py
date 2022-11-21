import aiosqlite
from os.path import exists

async def execute(query: str, *args) -> None:
    async with aiosqlite.connect("database.db") as db:
        await db.execute(query, *args)
        await db.commit()

async def fetch(query: str, *args) -> list:
    async with aiosqlite.connect("database.db") as db:
        cursor = await db.execute(query, *args)
        return await cursor.fetchall()

def __create_tables(cursor) -> None:

    # cursor.execute("""CREATE TABLE categories(
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name TEXT NOT NULL
    #     parent_id INTEGER NOT NULL
    # )""")

    # cursor.execute("""CREATE TABLE items(
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name TEXT NOT NULL,
    #     description TEXT,
    #     category_id INTEGER NOT NULL,
    #     FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE SET NULL,
    #     price REAL NOT NULL,
    #     images TEXT
    # )""")
    DB.commit()

def init() -> None:
    if exists("database.db"):
        return
