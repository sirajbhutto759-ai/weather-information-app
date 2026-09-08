# =============================================================================
# config.py — Application Configuration  [IMPROVED v2.0]
# =============================================================================
# Stores API credentials and application-level constants.
# IMPROVEMENT: API key loaded from environment variable for security.
#              Added VALID_UNITS tuple for input validation.
# =============================================================================

import os

# OpenWeatherMap API key — loaded from environment variable for security.
# Set it with:  set OPENWEATHER_API_KEY=your_key_here  (Windows)
#               export OPENWEATHER_API_KEY=your_key_here (Linux/Mac)
# Falls back to hardcoded key only for development/demo purposes.
API_KEY: str = os.environ.get(
    "OPENWEATHER_API_KEY",
    "your_api_key_here"  # fallback placeholder — set the env variable instead
)

# Base URL for the Current Weather Data endpoint
BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"

# Unit system: "metric" (°C), "imperial" (°F), or "standard" (K)
UNITS: str = "metric"

# Valid unit options for validation
VALID_UNITS: tuple = ("metric", "imperial", "standard")

# Request timeout in seconds
REQUEST_TIMEOUT: int = 10

# App display name and version
APP_NAME: str = "Weather Information Application"
APP_VERSION: str = "2.0.0"

# Exit commands recognised in the input loop
EXIT_COMMANDS: frozenset = frozenset({"quit", "exit", "q"})
