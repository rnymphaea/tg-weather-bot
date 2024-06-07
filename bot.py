import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods import DeleteWebhook

from config import TOKEN_BOT
from bot_interaction import base

class UserState(StatesGroup):
    city_choice = State()

bot = Bot(token=TOKEN_BOT)



async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(base.router)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())