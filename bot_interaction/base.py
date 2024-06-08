from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from bot import UserState
from config import API_WEATHER_TOKEN
from main import get_weather

router = Router()


@router.message(CommandStart())
async def start(message, state):
    user_full_name = message.from_user.full_name
    await state.set_state(UserState.city_choice)
    await message.answer(
        text=f"Приветствую вас, *{user_full_name}*.\nДля того, чтобы получить данные о погоде, напишите ваш город.", parse_mode="Markdown")
    

@router.message(UserState.city_choice)
async def send_weather(message, state):
    city = message.text
    try:
        data = get_weather(city, API_WEATHER_TOKEN)
        temperature = round(data["main"]["temp"])

        await message.answer(text=f"На данный момент в городе {city} температура составляет {temperature} °C")
    except Exception as err:
        print(err)
        await message.answer(text="Извините, мы не можем получить данные об этом городе!")


