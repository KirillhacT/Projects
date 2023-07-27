USE_ROUNDED_COORDS = True

OPEN_WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true&temperature_unit=celsius&timeformat=unixtime"
)
ADDRES = None
def GET_ADDRES() -> str:
    global ADDRES
    if ADDRES is None:
        ADDRES = input()
    else:
        return ADDRES


