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

def create_tables(database: aiosqlite.Connection, *tables: str) -> None:
    for table in tables:
        database.execute(table)
