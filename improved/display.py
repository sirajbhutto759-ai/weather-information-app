# =============================================================================
# display.py — Presentation Layer  [IMPROVED v2.0]
# =============================================================================
# Responsible for all terminal output. Uses ANSI escape codes for colour
# and formatting to create a polished, user-friendly CLI experience.
#
# IMPROVEMENTS:
#   - Encapsulated ANSI codes in an Enum/Class for better organisation
#   - Replaced hardcoded width values with a constant
#   - Refactored condition mapping to be more robust
# =============================================================================

from enum import Enum
from weather_parser import WeatherData

# IMPROVEMENT: Use a class/enum for colours instead of loose constants
class Color(str, Enum):
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[96m"
    BLUE    = "\033[94m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    WHITE   = "\033[97m"
    MAGENTA = "\033[95m"

    def __str__(self) -> str:
        return self.value


DISPLAY_WIDTH = 60

# Weather condition → ASCII art + colour mapping
CONDITION_MAP: dict[str, tuple[str, Color]] = {
    "clear":        ("☀️  Clear Sky",       Color.YELLOW),
    "clouds":       ("☁️  Cloudy",           Color.WHITE),
    "rain":         ("🌧️  Rain",             Color.BLUE),
    "drizzle":      ("🌦️  Drizzle",          Color.CYAN),
    "thunderstorm": ("⛈️  Thunderstorm",     Color.MAGENTA),
    "snow":         ("❄️  Snow",             Color.WHITE),
    "mist":         ("🌫️  Mist",             Color.WHITE),
    "fog":          ("🌫️  Fog",              Color.WHITE),
    "haze":         ("🌁  Haze",             Color.WHITE),
    "smoke":        ("💨  Smoke",            Color.DIM),
    "dust":         ("🌪️  Dust",             Color.YELLOW),
    "sand":         ("🌪️  Sand",             Color.YELLOW),
    "tornado":      ("🌪️  Tornado",          Color.RED),
}


def _get_condition_info(description: str) -> tuple[str, Color]:
    """Return (label, colour) tuple for a weather description string."""
    desc_lower = description.lower()
    for keyword, (label, colour) in CONDITION_MAP.items():
        if keyword in desc_lower:
            return label, colour
    return f"🌡️  {description.title()}", Color.CYAN


def _bar(value: int, max_value: int = 100, width: int = 20, colour: Color = Color.GREEN) -> str:
    """Render a simple ASCII progress bar."""
    if max_value <= 0:
        return ""
    
    filled = round((value / max_value) * width)
    filled = max(0, min(filled, width))
    bar_str = "█" * filled + "░" * (width - filled)
    return f"{colour}{bar_str}{Color.RESET}"


def print_banner(app_name: str, version: str) -> None:
    """Print the application banner on startup."""
    print()
    print(f"{Color.CYAN}═" * DISPLAY_WIDTH + str(Color.RESET))
    title = f"  🌤  {app_name}  v{version}"
    print(f"{Color.BOLD}{Color.CYAN}{title.center(DISPLAY_WIDTH)}{Color.RESET}")
    print(f"{Color.CYAN}═" * DISPLAY_WIDTH + str(Color.RESET))
    print()


def print_weather(weather: WeatherData) -> None:
    """
    Display formatted weather information for a city.

    Args:
        weather (WeatherData): Parsed weather data object.
    """
    condition_label, condition_colour = _get_condition_info(weather.description)
    divider = f"{Color.CYAN}─" * DISPLAY_WIDTH + str(Color.RESET)

    print(f"\n{divider}")
    header = f"  📍  {weather.city}, {weather.country}"
    print(f"{Color.BOLD}{Color.WHITE}{header.ljust(DISPLAY_WIDTH)}{Color.RESET}")
    print(f"  {condition_colour}{condition_label}{Color.RESET}")
    print(divider)

    # ── Temperature block ──
    unit = weather.temp_unit
    print(f"\n{Color.BOLD}  🌡  Temperature{Color.RESET}")
    print(f"      Current   : {Color.YELLOW}{Color.BOLD}{weather.temperature:.1f} {unit}{Color.RESET}")
    print(f"      Feels Like: {Color.YELLOW}{weather.feels_like:.1f} {unit}{Color.RESET}")
    print(f"      Min / Max : {Color.BLUE}{weather.temp_min:.1f}{Color.RESET} / {Color.RED}{weather.temp_max:.1f} {unit}{Color.RESET}")

    # ── Humidity block ──
    print(f"\n{Color.BOLD}  💧  Humidity{Color.RESET}")
    hum_bar = _bar(weather.humidity, 100, 20, Color.BLUE)
    print(f"      {hum_bar}  {Color.BLUE}{weather.humidity}%{Color.RESET}")

    # ── Wind block ──
    print(f"\n{Color.BOLD}  🌬  Wind{Color.RESET}")
    print(f"      Speed    : {Color.GREEN}{weather.wind_speed} {weather.speed_unit}{Color.RESET}")
    print(f"      Direction: {Color.GREEN}{weather.wind_direction}° ({weather.wind_compass}){Color.RESET}")

    # ── Additional details ──
    print(f"\n{Color.BOLD}  📊  Additional Details{Color.RESET}")
    print(f"      Pressure   : {Color.WHITE}{weather.pressure} hPa{Color.RESET}")
    print(f"      Cloudiness : {Color.WHITE}{weather.cloudiness}%{Color.RESET}")
    if weather.visibility > 0:
        print(f"      Visibility : {Color.WHITE}{weather.visibility_km} km{Color.RESET}")

    print(f"\n{divider}\n")


def print_error(message: str) -> None:
    """Display a formatted error message."""
    print(f"\n  {Color.RED}✖  Error: {message}{Color.RESET}\n")


def print_info(message: str) -> None:
    """Display a neutral informational message."""
    print(f"  {Color.DIM}{Color.WHITE}{message}{Color.RESET}")


def print_goodbye() -> None:
    """Display exit message."""
    print(f"\n{Color.CYAN}  👋  Thank you for using the Weather App. Goodbye!{Color.RESET}\n")
