from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from bot import UserState, bot
from config import API_WEATHER_TOKEN
from main import get_weather
from database import db

router = Router()


@router.message(CommandStart())
async def start(message, state):
    user_full_name = message.from_user.full_name
    await state.set_state(UserState.city_choice)
    await message.answer(
        text=f"Приветствую вас, *{user_full_name}*.\nДля того, чтобы получить данные о погоде, напишите ваш город.", parse_mode="Markdown")
    

@router.message(UserState.city_choice)
async def send_weather(message, state):
    city = str(message.text)
    try:
        data = get_weather(city, API_WEATHER_TOKEN)
        temperature = round(data["main"]["temp"])
        db.add_user_info({"telegram_id": message.from_user.id, "city": city})
        await message.answer(text=f"На данный момент в городе {city} температура составляет {temperature} °C")
    except Exception as err:
        print(err)
        await message.answer(text="Извините, мы не можем получить данные об этом городе!")


async def send_weather_to_all():
    data = db.get_users_data()
    for user_data in data:
        city = user_data["city"]
        w = get_weather(city, API_WEATHER_TOKEN)
        temperature = round(w["main"]["temp"])
        await bot.send_message(user_data["telegram_id"], text=f"На данный момент в городе {city} температура составляет {temperature} °C")

