import requests
import time
import sys
import os

# =========================================================================
# Configuration
# =========================================================================

# from OpenWeatherMap (https://openweathermap.org).
API_KEY = "ece175428d24a9e3e2b6d46d409a803c"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"  # Use "imperial" for Fahrenheit or "metric" for Celsius

# =========================================================================
# ASCII Art Definitions for Console Animation
# =========================================================================

# ASCII frames for Sun animation
SUN_FRAMES = [
    "  \\ O /  ",
    " -- O -- ",
    "  / O \\  ",
    " -- O -- ",
]

# ASCII frames for Rain animation
RAIN_FRAMES = [
    "  _`_`_  ",
    " ( /\\/ ) ",
    " |\\/\\/| ",
    " /\\|/\\/ ",
]

# Static Icons for other weather
WEATHER_ICONS = {
    "Clear": "☀️ Clear Sky",
    "Clouds": "☁️ Cloudy/Overcast",
    "Rain": "🌧️ Rainy",
    "Drizzle": "💦 Light Rain/Drizzle",
    "Thunderstorm": "⛈️ Stormy",
    "Snow": "❄️ Snowy",
    "Mist": "🌫️ Fog/Mist",
}


# =========================================================================
# Core Functions
# =========================================================================

def get_weather_data(location):
    """Fetches current weather data for the specified location."""

    # Construct the full API URL
    params = {
        'q': location,
        'appid': API_KEY,
        'units': UNITS
    }

    try:
        # Make the API request
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()

        # Check if the city was found
        if data.get("cod") == "404":
            return {"error": f"Location '{location}' not found."}

        return data

    except requests.exceptions.RequestException as e:
        # Handle connection errors or other request-related issues
        return {"error": f"API Request Error: {e}"}
    except Exception as e:
        # Handle parsing errors or unexpected issues
        return {"error": f"An unexpected error occurred: {e}"}


def display_weather_animation(condition_main):
    """Simulates a short console animation based on the main weather condition."""

    # Choose frames based on condition
    if condition_main in ["Rain", "Drizzle", "Thunderstorm", "Snow"]:
        frames = RAIN_FRAMES
        icon_name = "Rain/Snow"
    elif condition_main == "Clear":
        frames = SUN_FRAMES
        icon_name = "Sun"
    else:
        # For clouds, mist, etc., just print the icon once
        print(f"\n--- {WEATHER_ICONS.get(condition_main, condition_main)} Animation ---")
        return

    print(f"\n--- Simulating {icon_name} Animation ({condition_main}) ---")

    # Run the "animation" loop (5 cycles)
    for _ in range(5):
        for frame in frames:
            # Clear the previous lines and print the new frame
            # (Note: Clearing the console fully is complex and OS-dependent,
            # so we just overwrite the frame line using '\r' and time.sleep)
            print(f"\r{frame}", end='', flush=True)
            time.sleep(0.15)

    # Move to a new line after the animation is finished
    print("\n-------------------------------------------")


def display_weather_info(data):
    """Prints the extracted weather information."""

    if "error" in data:
        print("\n[ERROR]")
        print(data["error"])
        return

    main = data.get("main", {})
    weather = data.get("weather", [{}])[0]
    location_name = data.get("name", "Unknown Location")
    country = data.get("sys", {}).get("country", "")

    # Extract required information
    temperature = main.get("temp")
    humidity = main.get("humidity")
    weather_condition_main = weather.get("main", "N/A")
    weather_condition_desc = weather.get("description", "N/A").capitalize()

    unit_char = "C" if UNITS == "metric" else "F"

    # 1. Run the Animation
    display_weather_animation(weather_condition_main)

    # 2. Display the Data
    print(f"\n[ 🌍 Weather Report for {location_name}, {country} ]")
    print(f"=================================================")
    print(f"🌡️ Temperature: {temperature:.1f}°{unit_char}")
    print(f"💧 Humidity:    {humidity}%")
    print(f"☀️ Conditions:  {weather_condition_desc} ({weather_condition_main})")
    print(f"=================================================")


def main():
    """Main function to run the weather application."""
    print("--- Python Console Weather App ---")
    print("Fetching weather data using OpenWeatherMap.")

    if API_KEY == "YOUR_API_KEY_HERE":
        print(
            "\nCRITICAL ERROR: Please replace 'YOUR_API_KEY_HERE' in the script with your actual OpenWeatherMap API key.")
        return

    # Get user input for location
    location = input("\nEnter city name or ZIP code: ").strip()
    if not location:
        print("Location cannot be empty. Exiting.")
        return

    print(f"\nFetching data for {location}...")

    # Fetch and display
    weather_data = get_weather_data(location)
    display_weather_info(weather_data)


if __name__ == "__main__":
    main()
