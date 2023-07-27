from wether_api_service import Weather

def format_weather(weather: Weather) -> str:
    return (f"{weather.city}, температура {weather.temperature}°С, "
            f"{weather.weather_type.value}\n"
            f"Дата: {weather.time.strftime('%d.%m.%Y')}")
