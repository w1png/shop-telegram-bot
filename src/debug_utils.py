import random
import datetime
import string
import asyncio

import models
import constants
import database

ALL_CHARACTERS = string.ascii_letters + string.digits

async def create_random_user():
    id = random.randint(0, 1000000)
    username = ''.join(random.choice(ALL_CHARACTERS) for _ in range(10))
    date = datetime.datetime(
        random.randint(2020, 2022),
        random.randint(1, 12),
        random.randint(1, 28),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59),
    )
    await database.fetch("INSERT INTO users (id, username, date_created) VALUES (?,?,?)", id, username, date)


async def main():
    task = create_random_user
    tasks = [task() for _ in range(50)]
    await asyncio.gather(*tasks)



if __name__ == '__main__':
    asyncio.run(main())

