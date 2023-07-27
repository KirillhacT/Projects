from typing import NamedTuple
from geopy import Nominatim
from geopy.location import Location

from exceptions import CantGetCoordinates
import config

class Coordinates(NamedTuple):
    latitude: float
    longitude: float

def get_gps_coordinates() -> Coordinates:
    coordinates = _get_coordinates()
    return _round_coordinates(coordinates)

def _get_coordinates() -> Coordinates:
    locale = _get_currect_locale()
    return Coordinates(
        latitude=locale.latitude,
        longitude=locale.longitude,
    )

def _get_currect_locale() -> Location:
    locale = _get_locale()
    if locale is None:
        raise CantGetCoordinates
    return locale

def _get_locale() -> Location:
    geolocator = Nominatim(user_agent="run")
    locale = geolocator.geocode(config.ADDRES)
    return locale


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(*map(lambda x: round(x, 1), [
        coordinates.latitude,
        coordinates.longitude,
    ]))
