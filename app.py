import asyncio

from aiogram import executor

from handlers import dp, bot
from misc.scheduler import scheduler


async def on_startup(*args):
    asyncio.create_task(scheduler())


async def on_shutdown(*args):
    await bot.close()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
