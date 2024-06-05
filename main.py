import requests
from config import API_WEATHER_TOKEN

def get_weather(city: str, token: str):
    try:
        lat, lon = get_coordinates_by_name(city, token)
        request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}&units=metric&lang=ru")
        data = request.json()
        return data
    
    except Exception as e:
        print(f"Error in function get_weather: [ {e} ]!")    


def get_coordinates_by_name(city: str, token: str) -> tuple:
    try:
        request = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={token}")
        data = request.json()

    except Exception as e:
        print(f"Error in function get_coordinates_by_name: [ {e} ]")

    return (data["lat"], data["lon"])



def main():
    r = get_weather("London", API_WEATHER_TOKEN)
    print(r)


main()