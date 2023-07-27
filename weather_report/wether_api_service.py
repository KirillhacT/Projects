import datetime
from typing import NamedTuple
from enum import Enum
import urllib.request
from urllib.error import URLError
import json
from json.decoder import JSONDecodeError

from coordinates import Coordinates
from exceptions import ApiServiceError
import config

Celsius = int

class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморозь"
    RAIN = "Дождь"
    CLEAR = "Ясно"
    FOG = "Туман"
    CLOUDS = "Облачно"
    OVERCAST = "Пасмурно"
    FREEZING_DRIZZLE = "Моросящий дождь"
    FREEZING_RAIN = "Ледяной дождь"
    SNOW_FALL = "Снегопад"
    SNOW_GRAINS = "Снежные зерна"
    RAIN_SHOWERS = "Дождевые ливни"
    SNOW_SHOWERS = "Снежные ливни"

class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    time: datetime.datetime
    city: str

def get_weather(coordinates: Coordinates) -> Weather:
    open_weather_responce = _get_openweather_responce(
        latitude=coordinates.latitude, longitude=coordinates.longitude
    )
    weather = _parse_openweather_responce(open_weather_responce)
    return weather

def _get_openweather_responce(latitude: float, longitude: float) -> str:
    url = config.OPEN_WEATHER_URL.format(lat=latitude, long=longitude)
    try:
        text = urllib.request.urlopen(url).read()
        # print(text)
        return text
    except URLError:
        raise ApiServiceError

def _parse_openweather_responce(openweather_responce: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_responce)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        city=config.GET_ADDRES(),
        time=_parse_time(openweather_dict)
    )

def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict["current_weather"]["temperature"])

def _parse_time(openweather_dict: dict) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(openweather_dict["current_weather"]["time"])

def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["current_weather"]["weathercode"])
        # print(weather_type_id)
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
        "95 96 99": WeatherType.THUNDERSTORM,
        "51 53 55": WeatherType.DRIZZLE,
        "61 63 65": WeatherType.RAIN,
        "0 1": WeatherType.CLEAR,
        "45 48": WeatherType.FOG,
        "2": WeatherType.CLOUDS,
        "3": WeatherType.OVERCAST,
        "56 57": WeatherType.FREEZING_DRIZZLE,
        "66 67": WeatherType.FREEZING_RAIN,
        "71 73 75": WeatherType.SNOW_FALL,
        "77": WeatherType.SNOW_GRAINS,
        "80 81 82": WeatherType.RAIN_SHOWERS,
        "85 86": WeatherType.SNOW_SHOWERS,
    }
    for _numbers, _weather_type in weather_types.items():
        _numbers_list = _numbers.split(" ")
        if weather_type_id in _numbers_list:
            return _weather_type
    raise ApiServiceError
