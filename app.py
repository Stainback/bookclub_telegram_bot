import asyncio
import logging

from aiogram import executor

from handlers import dp, bot
from misc.scheduler import scheduler


async def on_startup(*args):
    asyncio.create_task(scheduler())
    logging.info("Bot is launched.")


async def on_shutdown(*args):
    await bot.close()
    logging.info("Bot is closed.")


if __name__ == "__main__":
    logging.basicConfig(filename="bot.log",
                        format='%(levelname)s: %(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
