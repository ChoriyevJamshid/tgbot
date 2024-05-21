import os
import time

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djconfig.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from handlers.users_private import users_private_router
from middlewares.middleware import SessionMiddleware

load_dotenv()

bot = Bot(token=os.environ.get('TOKEN'), parse_mode=ParseMode.HTML)
print(os.environ.get('TOKEN'))
dp = Dispatcher()
dp.include_router(users_private_router)


async def on_startup():
    print('Bot started...')


async def main():
    dp.startup.register(on_startup)

    dp.update.middleware(SessionMiddleware(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"Exception: {e}")
            time.sleep(15)
