import random
import datetime
import string
import asyncio

import models
import constants
import database

ALL_CHARACTERS = string.ascii_letters + string.digits

def create_random_date() -> datetime.datetime:
    return datetime.datetime(
        random.randint(2020, 2022),
        random.randint(1, 12),
        random.randint(1, 28),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59),
    )


async def create_random_user():
    id = random.randint(0, 1000000)
    username = ''.join(random.choice(ALL_CHARACTERS) for _ in range(10))
    date = create_random_date()
    await database.fetch("INSERT INTO users (id, username, date_created) VALUES (?,?,?)", id, username, date)


async def create_random_order():
    date = create_random_date()
    user_id = random.randint(0, 1000000)
    await database.fetch("INSERT INTO orders (user_id, items, date_created) VALUES (?,?,?)", user_id, "{}", date)


async def main():
    task = create_random_order
    tasks = [task() for _ in range(50)]
    await asyncio.gather(*tasks)



if __name__ == '__main__':
    asyncio.run(main())

