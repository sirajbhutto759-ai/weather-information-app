# 🌤 Weather Information Application

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![API](https://img.shields.io/badge/OpenWeatherMap-API-orange?style=for-the-badge&logo=cloudflare&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge)

A feature-rich, Python-based **command-line weather application** that delivers real-time weather data for any city worldwide using the [OpenWeatherMap API](https://openweathermap.org/api). Displays temperature, humidity, wind, pressure, and more — all with beautiful ANSI-coloured terminal output.

</div>

---

## 📸 Screenshots

| App Launch | Weather Results |
|---|---|
| ![App Launch](Screenshot%202026-06-24%20225756.png) | ![Weather Results](Screenshot%202026-07-02%20210738.png) |

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **City Search** | Search any city name worldwide for live weather data |
| 🌡️ **Temperature** | Current, feels-like, daily minimum and maximum |
| 💧 **Humidity** | Percentage with a visual ASCII progress bar |
| 🌬️ **Wind Info** | Speed (m/s / mph) and compass-direction bearing |
| 📊 **Extra Details** | Atmospheric pressure, cloudiness %, and visibility |
| 🎨 **ANSI Colour Output** | Polished, colour-coded terminal experience |
| 🔁 **Multi-search Loop** | Search multiple cities without restarting the app |
| 🛡️ **Robust Error Handling** | Invalid city, network issues, rate limits all handled gracefully |
| 📝 **Logging** | All activity logged to `weather_app.log` for debugging |
| 🗄️ **SQLite Schema** | Full relational database schema included (`schema_sqlite.sql`) |

---

## 📁 Project Structure

```
weather-information-app/
│
├── main.py               # Entry point — orchestrates the app loop
├── config.py             # API key, base URL, and global constants
├── weather_api.py        # HTTP layer — fetches data from OpenWeatherMap
├── weather_parser.py     # JSON → WeatherData dataclass conversion
├── display.py            # ANSI-coloured terminal presentation layer
│
├── schema_sqlite.sql     # Full SQLite relational database schema
├── index.html            # Web-based interface (HTML)
├── er_diagram.png        # Entity-Relationship diagram
│
├── improved/             # Version 2.0 refactored module copies
│   ├── config.py
│   ├── display.py
│   ├── main.py
│   ├── weather_api.py
│   └── weather_parser.py
│
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** — [Download here](https://www.python.org/downloads/)
- A free **OpenWeatherMap API key** — [Get one here](https://openweathermap.org/api)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/weather-information-app.git
cd weather-information-app
```

### 2. Create & Activate a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key

The app reads your API key from an **environment variable** (most secure approach):

**Windows (Command Prompt):**
```cmd
set OPENWEATHER_API_KEY=your_actual_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:OPENWEATHER_API_KEY="your_actual_api_key_here"
```

**macOS / Linux:**
```bash
export OPENWEATHER_API_KEY="your_actual_api_key_here"
```

> **Alternative:** Open `config.py` and replace `"your_api_key_here"` with your key directly (not recommended for shared environments).

### 5. Run the Application

```bash
python main.py
```

---

## 🖥️ Usage

```
════════════════════════════════════════════════════════════
                🌤  Weather Information Application  v2.0.0
════════════════════════════════════════════════════════════

  Type a city name to get current weather information.
  Type 'quit' or 'exit' or press Ctrl+C to close the app.

  🔍  Enter city name: London

────────────────────────────────────────────────────────────
  📍  London, GB
  ☁️  Cloudy
────────────────────────────────────────────────────────────

  🌡  Temperature
      Current   : 18.3 °C
      Feels Like: 17.8 °C
      Min / Max : 15.2 / 21.0 °C

  💧  Humidity
      ████████░░░░░░░░░░░░  68%

  🌬  Wind
      Speed    : 4.2 m/s
      Direction: 230° (SW)

  📊  Additional Details
      Pressure   : 1012 hPa
      Cloudiness : 75%
      Visibility : 10.0 km
```

### Commands

| Input | Action |
|---|---|
| Any city name | Fetch and display weather |
| `quit` / `exit` / `q` | Exit the application |
| `Ctrl+C` | Exit the application |

---

## ⚙️ Configuration (`config.py`)

| Setting | Type | Default | Description |
|---|---|---|---|
| `OPENWEATHER_API_KEY` | `str` (env var) | — | Your OpenWeatherMap API key |
| `UNITS` | `str` | `"metric"` | `"metric"` (°C), `"imperial"` (°F), `"standard"` (K) |
| `REQUEST_TIMEOUT` | `int` | `10` | HTTP request timeout in seconds |
| `APP_NAME` | `str` | `"Weather Information Application"` | Display name |
| `APP_VERSION` | `str` | `"2.0.0"` | Application version |

---

## 🗄️ Database Schema

The project includes a full **SQLite relational schema** (`schema_sqlite.sql`) designed to persist weather search history:

```
users ──< search_history >── locations
                 │
                 └──< weather_records >── weather_conditions
```

| Table | Purpose |
|---|---|
| `users` | User accounts |
| `locations` | City + country records |
| `weather_conditions` | Standardised condition catalogue |
| `search_history` | Log of every search performed |
| `weather_records` | Full weather snapshot per search |

To initialise the database:
```bash
sqlite3 weather_app.db < schema_sqlite.sql
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `requests` | 2.32.3 | HTTP requests to OpenWeatherMap API |

> All other modules (`dataclasses`, `logging`, `os`, `sys`) are Python standard library.

---

## 🛠️ Error Handling

| Scenario | Behaviour |
|---|---|
| Empty input | Prompts user to enter a valid city name |
| Invalid city name | Friendly "City not found" message (HTTP 404) |
| Invalid / missing API key | Clear instructions to set the environment variable |
| Network connection error | Descriptive connectivity error message |
| API rate limit exceeded | Notifies user to wait before retrying |
| Request timeout | Reports timeout with retry suggestion |
| Malformed API response | `WeatherParseError` with field identification |
| Any unexpected error | Caught gracefully, logged, user shown a safe message |

---

## 🏗️ Architecture

The application follows a clean **layered architecture**:

```
┌─────────────────────────────────┐
│          main.py (Entry)        │  ← User I/O loop & orchestration
├─────────────────────────────────┤
│        weather_api.py           │  ← HTTP / Network layer
├─────────────────────────────────┤
│       weather_parser.py         │  ← Data transformation layer
├─────────────────────────────────┤
│         display.py              │  ← Presentation / UI layer
├─────────────────────────────────┤
│          config.py              │  ← Configuration & constants
└─────────────────────────────────┘
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [OpenWeatherMap](https://openweathermap.org/) for providing the free weather API
- [Python Requests library](https://docs.python-requests.org/) for simplified HTTP calls

---

<div align="center">

Made with ❤️ by **Muhammad Siraj**

</div>
