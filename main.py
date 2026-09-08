# =============================================================================
# main.py — Application Entry Point  [IMPROVED v2.0]
# =============================================================================
# Orchestrates the user-input loop, delegates to the API and parser layers,
# and calls the display layer to present results.
#
# IMPROVEMENTS:
#   - Added standard logging configuration
#   - Refactored main loop into smaller functions for better testability
#   - Used structural pattern matching (if applicable) / better exit conditions
#   - Proper type hints for main loop
# =============================================================================

import sys
import io
import logging

# Windows terminal UTF-8 fix
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from config import APP_NAME, APP_VERSION, EXIT_COMMANDS, UNITS
from weather_api import fetch_weather, WeatherAPIError
from weather_parser import parse_weather, WeatherParseError
from display import (
    print_banner,
    print_weather,
    print_error,
    print_info,
    print_goodbye,
)

# Configure standard logging (writes to file instead of messing up the CLI)
logging.basicConfig(
    filename='weather_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def process_city_search(city: str) -> None:
    """
    Handle the fetching, parsing, and displaying of weather data for a single city.
    
    IMPROVEMENT: Extracted from the main loop to make it testable and readable.
    """
    print_info(f"Fetching weather data for '{city}'...")
    logger.info("User searched for city: %s", city)

    try:
        raw_data = fetch_weather(city)
        weather = parse_weather(raw_data, unit_system=UNITS)
        print_weather(weather)
        logger.info("Successfully displayed weather for: %s", city)

    except WeatherAPIError as e:
        print_error(str(e))
        logger.warning("API Error for '%s': %s", city, e)
    
    except WeatherParseError as e:
        print_error(str(e))
        logger.error("Parse Error for '%s': %s", city, e)
        
    except Exception as e:
        # Catch-all for unexpected bugs
        print_error("An unexpected system error occurred. Please try again.")
        logger.exception("Unexpected error processing city '%s': %s", city, e)


def prompt_user_to_continue() -> bool:
    """Prompt the user if they want to search again."""
    try:
        again = input("  🔄  Search another city? (yes/no): ").strip().lower()
        return again in {"yes", "y"}
    except (KeyboardInterrupt, EOFError):
        return False


def run() -> None:
    """Main application interactive loop."""
    print_banner(APP_NAME, APP_VERSION)
    print_info("Type a city name to get current weather information.")
    print_info("Type 'quit' or 'exit' or press Ctrl+C to close the app.\n")

    logger.info("Application started (v%s)", APP_VERSION)

    while True:
        try:
            city = input("  🔍  Enter city name: ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        # Exit condition
        if city.lower() in EXIT_COMMANDS:
            break

        # Validation
        if not city:
            print_error("Please enter a valid city name.")
            continue

        # Process the city
        process_city_search(city)

        # Prompt for next action
        if not prompt_user_to_continue():
            break
        print()

    print_goodbye()
    logger.info("Application closed cleanly by user.")
    sys.exit(0)


if __name__ == "__main__":
    run()
