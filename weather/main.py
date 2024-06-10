import requests

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
        if not data:
            print("Error in function get_coordinates_by_name: cannot get info about this city!\n")
            return 
        else:
            data = data[0]

    except Exception as e:
        print(f"Error in function get_coordinates_by_name: [ {e} ]")

    return (data["lat"], data["lon"])

