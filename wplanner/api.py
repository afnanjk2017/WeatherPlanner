import openmeteo_requests
import arrow
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
places = {"Qassim University":[26.3489 , 43.7668],
          "Riyadh": [24.7136 ,46.6753],
          "Jeddah":[21.5292 , 39.1611],}

def gett( place: str , date: str , Hour : int) :
    params = {
	 "latitude": places[place][0],
        "longitude": places[place][1],
        "hourly": ["temperature_2m" ,"rain", "wind_speed_10m"], 
        "wind_speed_unit": "ms",  
        "start_date": date,
        "end_date": date,
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
   

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_rain = hourly.Variables(1).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()

    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    info = [hourly_temperature_2m[Hour],hourly_wind_speed_10m[Hour],hourly_rain[Hour]]
    
    return info











# Process first location. Add a for-loop for multiple locations or weather models


""" hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s"),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe) """








