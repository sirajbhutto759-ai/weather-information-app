# =============================================================================
# weather_parser.py — JSON Data Processing Layer  [IMPROVED v2.0]
# =============================================================================
# Extracts and structures the relevant fields from the raw OpenWeatherMap
# JSON response into a clean WeatherData dataclass.
#
# IMPROVEMENTS:
#   - WeatherData made immutable with frozen=True
#   - temp_unit and speed_unit decoupled from global UNITS (passed as field)
#   - parse_weather raises descriptive ParseError instead of raw KeyError
#   - Safer data access with .get() for all optional API fields
# =============================================================================

from __future__ import annotations
from dataclasses import dataclass, field


class WeatherParseError(Exception):
    """Raised when the API response is missing expected fields."""
    pass


# Mapping of unit system → (temp symbol, speed unit)
_UNIT_SYMBOLS: dict[str, tuple[str, str]] = {
    "metric":   ("°C", "m/s"),
    "imperial": ("°F", "mph"),
    "standard": ("K",  "m/s"),
}

_COMPASS_POINTS: list[str] = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
]


@dataclass(frozen=True)
class WeatherData:
    """
    Immutable container for parsed weather information.

    IMPROVEMENT: frozen=True prevents accidental mutation after creation.
    IMPROVEMENT: unit_system stored as a field so properties are self-contained
                 and do not depend on the global config at call time.
    """
    city:           str
    country:        str
    temperature:    float
    feels_like:     float
    temp_min:       float
    temp_max:       float
    humidity:       int
    description:    str
    wind_speed:     float
    wind_direction: int
    visibility:     int     # in metres
    cloudiness:     int     # percentage
    pressure:       int     # hPa
    unit_system:    str = field(default="metric")

    @property
    def temp_unit(self) -> str:
        """Return the temperature unit symbol."""
        return _UNIT_SYMBOLS.get(self.unit_system, ("°C", "m/s"))[0]

    @property
    def speed_unit(self) -> str:
        """Return the wind-speed unit."""
        return _UNIT_SYMBOLS.get(self.unit_system, ("°C", "m/s"))[1]

    @property
    def visibility_km(self) -> float:
        """Convert visibility from metres to kilometres."""
        return round(self.visibility / 1000, 1)

    @property
    def wind_compass(self) -> str:
        """Convert wind direction in degrees to a compass point."""
        index = round(self.wind_direction / 22.5) % 16
        return _COMPASS_POINTS[index]


def parse_weather(data: dict, unit_system: str = "metric") -> WeatherData:
    """
    Parse raw JSON API data into a WeatherData object.

    IMPROVEMENT: Raises WeatherParseError (not raw KeyError) with a clear
                 message identifying which field is missing.

    Args:
        data        (dict): The raw JSON response from OpenWeatherMap.
        unit_system (str):  The unit system used for the API call.

    Returns:
        WeatherData: A structured, immutable weather data object.

    Raises:
        WeatherParseError: If expected fields are missing from the response.
    """
    try:
        return WeatherData(
            city=data["name"],
            country=data["sys"]["country"],
            temperature=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            temp_min=data["main"]["temp_min"],
            temp_max=data["main"]["temp_max"],
            humidity=data["main"]["humidity"],
            description=data["weather"][0]["description"].capitalize(),
            wind_speed=data["wind"]["speed"],
            wind_direction=data["wind"].get("deg", 0),
            visibility=data.get("visibility", 0),
            cloudiness=data["clouds"]["all"],
            pressure=data["main"]["pressure"],
            unit_system=unit_system,
        )
    except KeyError as exc:
        raise WeatherParseError(
            f"Unexpected API response format — missing field: {exc}"
        ) from exc
