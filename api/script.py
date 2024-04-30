import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import json
import mysql.connector

# Load in Script
load_dotenv(dotenv_path="../.env")
api_key = os.getenv("APIKEY")

# Database Connection setup
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="floodsight"
)

cursor = db.cursor()

insert_statement = """
INSERT INTO weather_data (date, dew_point, max_temp, min_temp, max_wind_speed, precipitation, avg_temp, wind_speed, prediction)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Niamey Niger Coordinates
lat = 13.5137
lon = 2.1098
units = "imperial"

end_date = datetime.now()
for i in range(30):
    target_date = end_date - timedelta(days=i)
    unix_timestamp = int(target_date.timestamp())

    # Timemachine Endpoint
    timemachine_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    timemachine_params = {
        "lat": lat,
        "lon": lon,
        "dt": unix_timestamp,
        "appid": api_key,
        "units": units,
    }
    tm_response = requests.get(timemachine_url, params=timemachine_params)
    tm_response.raise_for_status()
    tm_data = tm_response.json()

    # Daysummary Endpoint
    daysummary_url = "https://api.openweathermap.org/data/3.0/onecall/day_summary"
    daysummary_params = {
        "lat": lat,
        "lon": lon,
        "date": target_date.date(),
        "appid": api_key,
        "units": units,
    }
    ds_response = requests.get(daysummary_url, params=daysummary_params)
    ds_response.raise_for_status()
    ds_data = ds_response.json()

    DEWP = tm_data["data"][0]["dew_point"]
    MAX = ds_data["temperature"]["max"]
    MIN = ds_data["temperature"]["min"]
    MXSPD = ds_data["wind"]["max"]["speed"]
    PRCP = ds_data["precipitation"]["total"]
    TEMP = (MAX + MIN) / 2
    WDSP = tm_data["data"][0]["wind_speed"]
    prediction = None

    cursor.execute(
        insert_statement,
        (
            target_date.strftime("%Y-%m-%d"),
            DEWP,
            MAX,
            MIN,
            MXSPD,
            PRCP,
            TEMP,
            WDSP,
            prediction,
        ),
    )

db.commit()
cursor.close()
db.close()
