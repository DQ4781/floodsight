import requests
import os
from dotenv import load_dotenv
import json


def get_weather_data(api_key):
    # Niamey Niger Coordinates
    lat = 13.5137
    lon = 2.1098
    units = "imperial"

    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "units": units,
        "appid": api_key,
        "exclude": "current,minutely,hourly,alerts",
        "units": units,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return data


# Load in APIKEY from .env
load_dotenv(dotenv_path="../.env")
api_key = os.getenv("APIKEY")


weather_data = get_weather_data(api_key)

with open("niamey.json", "w") as file:
    json.dump(weather_data, file)
