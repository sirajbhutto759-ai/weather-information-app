# =============================================================================
# weather_api.py — API Integration Layer  [IMPROVED v2.0]
# =============================================================================
# Responsible for making HTTP requests to OpenWeatherMap and returning raw
# JSON data. All network-related exceptions are caught and re-raised as
# descriptive application-level errors.
#
# IMPROVEMENTS:
#   - Added startup API key validation
#   - Used response.raise_for_status() pattern with specific overrides
#   - Added logging support for debugging
#   - Removed redundant double-strip check
# =============================================================================

import logging
import requests
from config import API_KEY, BASE_URL, UNITS, REQUEST_TIMEOUT

# Module-level logger — controlled by the root logger in main.py
logger = logging.getLogger(__name__)

# HTTP status codes mapped to user-friendly messages
_HTTP_ERRORS: dict[int, str] = {
    401: "Invalid API key. Please update your key in config.py and try again.",
    404: "City '{city}' not found. Please check the spelling and try again.",
    429: "API rate limit exceeded. Please wait a moment and try again.",
}


class WeatherAPIError(Exception):
    """Raised for all weather-API related failures."""
    pass


def _validate_api_key() -> None:
    """
    Raise WeatherAPIError if the API key is empty or still the placeholder.

    Raises:
        WeatherAPIError: If API_KEY is not configured.
    """
    if not API_KEY or API_KEY == "your_api_key_here":
        raise WeatherAPIError(
            "API key is not configured. "
            "Set the OPENWEATHER_API_KEY environment variable."
        )


def fetch_weather(city_name: str) -> dict:
    """
    Fetch current weather data for a given city from OpenWeatherMap.

    Args:
        city_name (str): The name of the city to search for.

    Returns:
        dict: Parsed JSON response from the API.

    Raises:
        WeatherAPIError: On network errors, invalid city, or API key issues.
    """
    # IMPROVEMENT: Single strip — city_name already stripped by caller
    city_name = city_name.strip()
    if not city_name:
        raise WeatherAPIError("City name cannot be empty.")

    _validate_api_key()

    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": UNITS,
    }

    logger.debug("Fetching weather for '%s' (units=%s)", city_name, UNITS)

    try:
        response = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise WeatherAPIError(
            "Network error: Unable to connect. Please check your internet connection."
        )
    except requests.exceptions.Timeout:
        raise WeatherAPIError(
            f"Request timed out after {REQUEST_TIMEOUT} seconds. Try again later."
        )
    except requests.exceptions.RequestException as exc:
        raise WeatherAPIError(f"Unexpected network error: {exc}") from exc

    # Handle HTTP-level errors using the lookup table
    if response.status_code != 200:
        message = _HTTP_ERRORS.get(
            response.status_code,
            f"Unexpected API response (HTTP {response.status_code}): {response.text}",
        )
        # Insert city name into the 404 template if present
        raise WeatherAPIError(message.format(city=city_name))

    logger.debug("Weather data received for '%s'.", city_name)
    return response.json()
