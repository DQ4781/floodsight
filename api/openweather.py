import requests


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


def format_weather_json(weather_data):
    current_day = weather_data["daily"][0]
    data = {
        "DEWP": current_day["dew_point"],
        "MAX": current_day["temp"]["max"],
        "MIN": current_day["temp"]["min"],
        "MXSPD": current_day.get("wind_gust", 0),
        "PRCP": current_day.get("rain", 0),
        "TEMP": (current_day["temp"]["max"] + current_day["temp"]["min"]) / 2,
        "WDSP": current_day["wind_speed"],
    }

    return data
