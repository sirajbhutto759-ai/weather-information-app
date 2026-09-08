-- =============================================================================
-- schema_sqlite.sql — Weather Information Application (SQLite Version)
-- =============================================================================
-- Author      : Muhammad Siraj
-- Application : Weather Information Application v1.0.0
-- Database    : SQLite 3
-- =============================================================================

PRAGMA foreign_keys = ON;

-- Drop existing tables in reverse dependency order
DROP TABLE IF EXISTS weather_records;
DROP TABLE IF EXISTS search_history;
DROP TABLE IF EXISTS weather_conditions;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS users;

-- =============================================================================
-- TABLE: users
-- =============================================================================
CREATE TABLE users (
    user_id     INTEGER     PRIMARY KEY AUTOINCREMENT,
    username    TEXT        NOT NULL UNIQUE,
    email       TEXT        NOT NULL UNIQUE,
    created_at  TEXT        NOT NULL DEFAULT (datetime('now')),
    last_active TEXT        NOT NULL DEFAULT (datetime('now'))
);

-- =============================================================================
-- TABLE: locations
-- =============================================================================
CREATE TABLE locations (
    location_id     INTEGER     PRIMARY KEY AUTOINCREMENT,
    city_name       TEXT        NOT NULL,
    country_code    TEXT        NOT NULL,
    latitude        REAL        NULL,
    longitude       REAL        NULL,
    timezone_offset INTEGER     NULL,

    CONSTRAINT uq_locations_city UNIQUE (city_name, country_code)
);

-- =============================================================================
-- TABLE: weather_conditions
-- =============================================================================
CREATE TABLE weather_conditions (
    condition_id          INTEGER     PRIMARY KEY AUTOINCREMENT,
    condition_main        TEXT        NOT NULL,
    condition_description TEXT        NOT NULL UNIQUE,
    icon_code             TEXT        NULL
);

-- =============================================================================
-- TABLE: search_history
-- =============================================================================
CREATE TABLE search_history (
    search_id        INTEGER     PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER     NOT NULL,
    location_id      INTEGER     NULL,
    search_term      TEXT        NOT NULL,
    search_timestamp TEXT        NOT NULL DEFAULT (datetime('now')),
    was_successful   INTEGER     NOT NULL DEFAULT 0,   -- 0 = FALSE, 1 = TRUE

    CONSTRAINT fk_search_user     FOREIGN KEY (user_id)
        REFERENCES users (user_id)     ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_search_location FOREIGN KEY (location_id)
        REFERENCES locations (location_id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- =============================================================================
-- TABLE: weather_records
-- =============================================================================
CREATE TABLE weather_records (
    record_id       INTEGER     PRIMARY KEY AUTOINCREMENT,
    search_id       INTEGER     NOT NULL UNIQUE,   -- 1:1 with search_history
    location_id     INTEGER     NOT NULL,
    condition_id    INTEGER     NOT NULL,

    -- Temperature
    temperature     REAL        NOT NULL,
    feels_like      REAL        NOT NULL,
    temp_min        REAL        NOT NULL,
    temp_max        REAL        NOT NULL,
    unit_system     TEXT        NOT NULL DEFAULT 'metric'
                                CHECK (unit_system IN ('metric','imperial','standard')),

    -- Atmospheric
    humidity        INTEGER     NOT NULL CHECK (humidity BETWEEN 0 AND 100),
    pressure        INTEGER     NOT NULL,
    visibility_m    INTEGER     NULL,
    cloudiness      INTEGER     NOT NULL CHECK (cloudiness BETWEEN 0 AND 100),

    -- Wind
    wind_speed      REAL        NOT NULL,
    wind_direction  INTEGER     NULL CHECK (wind_direction IS NULL OR wind_direction BETWEEN 0 AND 360),

    recorded_at     TEXT        NOT NULL DEFAULT (datetime('now')),

    CONSTRAINT fk_wr_search    FOREIGN KEY (search_id)
        REFERENCES search_history (search_id)    ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_wr_location  FOREIGN KEY (location_id)
        REFERENCES locations (location_id)       ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_wr_condition FOREIGN KEY (condition_id)
        REFERENCES weather_conditions (condition_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- =============================================================================
-- INDEXES
-- =============================================================================
CREATE INDEX idx_search_history_user_id
    ON search_history (user_id, search_timestamp);

CREATE INDEX idx_search_history_location_id
    ON search_history (location_id, search_timestamp);

CREATE INDEX idx_weather_records_location_time
    ON weather_records (location_id, recorded_at);

-- =============================================================================
-- SEED DATA
-- =============================================================================

-- Common weather conditions from OpenWeatherMap
INSERT INTO weather_conditions (condition_main, condition_description, icon_code) VALUES
    ('Clear',        'clear sky',                   '01d'),
    ('Clouds',       'few clouds',                  '02d'),
    ('Clouds',       'scattered clouds',            '03d'),
    ('Clouds',       'broken clouds',               '04d'),
    ('Clouds',       'overcast clouds',             '04d'),
    ('Drizzle',      'light intensity drizzle',     '09d'),
    ('Drizzle',      'drizzle',                     '09d'),
    ('Rain',         'light rain',                  '10d'),
    ('Rain',         'moderate rain',               '10d'),
    ('Rain',         'heavy intensity rain',        '10d'),
    ('Thunderstorm', 'thunderstorm with light rain','11d'),
    ('Thunderstorm', 'thunderstorm',                '11d'),
    ('Snow',         'light snow',                  '13d'),
    ('Snow',         'snow',                        '13d'),
    ('Mist',         'mist',                        '50d'),
    ('Fog',          'fog',                         '50d'),
    ('Haze',         'haze',                        '50d'),
    ('Smoke',        'smoke',                       '50d'),
    ('Dust',         'dust',                        '50d'),
    ('Tornado',      'tornado',                     '50d');

-- Default user for the CLI application
INSERT INTO users (username, email) VALUES
    ('default_user', 'user@weatherapp.local');

-- =============================================================================
-- END OF SCHEMA
-- =============================================================================
