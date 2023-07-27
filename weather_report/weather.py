from pathlib import Path
import config
from coordinates import get_gps_coordinates
from exceptions import CantGetCoordinates, ApiServiceError
from wether_api_service import get_weather
from weather_formatter import format_weather
from history import save_weather, JSONFileWeatherStorage

def main():
    config.GET_ADDRES()
    try:
        coordinates = get_gps_coordinates()
    except CantGetCoordinates:
        print("Не удалось получить GPS координаты")
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print(f"Не удалось получить погоду по координатам {coordinates}")
        exit(1)
    print(format_weather(weather))
    save_weather(
        weather,
        JSONFileWeatherStorage(Path.cwd() / "history.json")
    )

if __name__ == '__main__':
    main()