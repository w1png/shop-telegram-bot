import aiosqlite


async def fetch(query: str, *args) -> list:
    async with aiosqlite.connect("database.db") as db:
        cursor = await db.execute(query, args)
        await db.commit()
        return list(await cursor.fetchall())

