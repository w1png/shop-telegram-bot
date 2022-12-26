from random import randint
import database
import models

async def create_categories(amount: int) -> None:
    for i in range(amount):
        await models.categories.create(f"Category {i}", i - randint(0, amount))


async def create_items(amount: int) -> None:
    for i in range(amount):
        await models.items.create(
            name=f"Item {i}",
            description=f"Description {i}",
            category_id=randint(0, amount),
            price=randint(0, 100000),
        )


async def get_users() -> list[models.users.User]:
    return [models.users.User(id) for id in (await database.fetch("SELECT id FROM users"))]


