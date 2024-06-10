import asyncio
import logging
import os


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods import DeleteWebhook
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import load_dotenv

load_dotenv()

from bot_interaction import base
from database.db import create_db

class UserState(StatesGroup):
    city_choice = State()
    interaction = State()
    change_city = State()

bot = Bot(token=os.getenv("TOKEN_BOT"))



async def main():
    logging.basicConfig(level=logging.INFO)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(base.router)

    create_db()
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(base.send_weather_to_all, 'cron', hour='10,12,14,16,18,20,22')
    scheduler.start()

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())