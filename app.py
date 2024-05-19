import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djconfig.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv, find_dotenv
from handlers.private import private_router

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)

dp = Dispatcher()
dp.include_router(private_router)


async def on_startup():
    print('Bot started...')





async def main():
    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
