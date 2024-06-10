import os

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from bot import UserState, bot
from weather.main import get_weather
from database import db

router = Router()

API_WEATHER_TOKEN = os.getenv("API_WEATHER_TOKEN")


@router.message(CommandStart())
async def start(message, state):
    user_full_name = message.from_user.full_name
    await state.set_state(UserState.city_choice)
    await message.answer(
        text=f"Приветствую вас, *{user_full_name}*.\nДля того, чтобы получить данные о погоде, напишите ваш город.", parse_mode="Markdown")
    

@router.message(UserState.city_choice)
async def send_weather(message, state: FSMContext):
    city = str(message.text)
    try:
        data = get_weather(city, API_WEATHER_TOKEN)
        text_to_send = text_weather(data, city)
        db.add_user_info({"telegram_id": message.from_user.id, "city": city})
        await state.set_state(UserState.interaction)
        await message.answer(text=text_to_send)
    except Exception:
        await message.answer(text="Извините, мы не можем получить данные об этом городе! Введите название ещё раз.")


@router.message(UserState.interaction, Command("change"))
async def change_city(message, state: FSMContext):
    await state.set_state(UserState.change_city)
    await message.answer(text="Введите название города.")


@router.message(UserState.interaction)
async def help(message, state: FSMContext):
    await message.answer(text="Вы уже ввели город, уведомления о погоде в котором хотите получать!\nЕсли хотите поменять город, введите команду /change")


@router.message(UserState.change_city)
async def change_city(message, state: FSMContext):
    city = str(message.text)
    s = await state.get_state()
    try:
        data = get_weather(city, API_WEATHER_TOKEN)
        text_to_send = text_weather(data, city)
        db.update_user_info({"telegram_id": message.from_user.id, "city": city})
        await state.set_state(UserState.interaction)
        await message.answer(text=text_to_send)
    except Exception:
        await message.answer(text="Извините, мы не можем получить данные об этом городе! Введите название ещё раз.")


async def send_weather_to_all():
    data = db.get_users_data()
    for user_data in data:
        city = user_data["city"]
        w = get_weather(city, API_WEATHER_TOKEN)
        temperature = round(w["main"]["temp"])
        await bot.send_message(user_data["telegram_id"], text=f"На данный момент в городе {city} температура составляет {temperature} °C")


def text_weather(data: dict, city: str):
    description = data["weather"][0]["description"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    temperature = round(data["main"]["temp"])
    text = f"На данный момент в городе {city} температура составляет {temperature} °C, {description}.\nСкорость ветра составляет {wind_speed} м/с.\nДавление - {pressure} мм рт.с."
    return text
