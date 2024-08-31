import asyncio
import os
import json

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from middlewares import AiohttpSessionMiddleware

from TG.user.handlers import router as user_main_router





bot = Bot(token = os.getenv("TOKEN"))
dp = Dispatcher()

dp.include_router(user_main_router)





async def on_startup(bot):
    print("Bot was started.")

async def on_shutdown(bot):
    print("Bot was down.")


user_commands = [
    BotCommand(command='start', description='начать работу с ботом'),
    
]

async def main()->None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(AiohttpSessionMiddleware())

    
    await bot.delete_webhook(drop_pending_updates = True)
    await bot.set_my_description("/start - начать работу")
    await bot.set_my_commands(commands = user_commands,scope = types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())