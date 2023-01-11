import aioschedule
import asyncio
import os, shutil
from datetime import datetime


async def scheduler(func: callable) -> None:
    aioschedule.every().day.at("00:00").do(func)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def __backup() -> None:
    print('Backup started at', datetime.now())

    backup_dir = f"backup/{datetime.now().strftime('%Y-%m-%d')}"
    if not os.path.exists("backup"):
        os.makedirs("backup")
    else:
        print('Backup folder already exists.\nSkipping...')
        return
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    shutil.copy("config.json", backup_dir)
    shutil.copy("database.db", backup_dir)

async def on_startup(_) -> None:
    asyncio.create_task(scheduler(__backup))
