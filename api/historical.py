import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta


# Load in API key
load_dotenv("../.env")
api_key = os.getenv("APIKEY")

# Niamey Niger Coordinates
lat = 13.5137
lon = 2.1098
units = "imperial"


end_date = datetime.now()
start_date = end_date - timedelta(days=30)

unix_timestamp = int(start_date.timestamp())

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

# Day Summary Endpoint
daysummary_url = "https://api.openweathermap.org/data/3.0/onecall/day_summary"
daysummary_params = {
    "lat": lat,
    "lon": lon,
    "date": start_date.date(),
    "appid": api_key,
    "units": units,
}
ds_response = requests.get(daysummary_url, params=daysummary_params)
ds_response.raise_for_status()
ds_data = ds_response.json()

with open("timemachine.json", "w") as f:
    json.dump(tm_data, f)

with open("daysummary.json", "w") as f:
    json.dump(ds_data, f)
