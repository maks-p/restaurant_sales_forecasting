import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
import time

from config import darksky_api_key

# Try / Except Helper Function for Handling JSON API Output
def find_val(dictionary, *keys):
    level = dictionary

    for key in keys:
        try:
            level = level[key]
        except:
            return np.NAN
    return level

# Create List of Dates of target Weather Data
def date_range(start_date, end_date):
    list_of_days = []
    daterange = pd.date_range(start_date, end_date)
    for single_date in daterange:
        list_of_days.append(single_date.strftime("%Y-%m-%d"))

    return list_of_days

class Weather:

    check_time = '19:30:00'

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def make_api_call(self, day):
        base_url = 'https://api.darksky.net/forecast/'
        time_ = 'T' + Weather.check_time
        url = f'{base_url}{darksky_api_key}/{self.latitude},{self.longitude},{day + time_}?America/New_York&exclude=flags'
            
        return requests.get(url).json()

    def daily_weather(self, day):
        r = self.make_api_call(day)

        # Convert Time Return to Datetime from Epoch
        time = datetime.fromtimestamp(r['currently']['time']).strftime('%Y-%m-%d')

        # Get precipIntensityMaxTime unless there is none, then encode as 5:01 AM for now.
        try:
            precip_max_time = datetime.fromtimestamp(find_val(r, 'daily', 'data', 0, 'precipIntensityMaxTime')).strftime('%I:%M%p')
        except:
            precip_max_time = datetime(1900,1,1,5,1).strftime('%I:%M%p')
        
        # Unpack DarkSky API using Helper Function
        entry = {'date': time,
                'temperature': float(find_val(r, 'currently', 'temperature')),
                'apparent_temperature': float(find_val(r, 'currently', 'apparentTemperature')),
                'humidity': float(find_val(r, 'currently', 'humidity')),
                'precip_intensity_max': float(find_val(r,'daily','data', 0, 'precipIntensityMax')),
                'precip_type': find_val(r, 'daily', 'data', 0, 'precipType'),
                'precip_prob': float(find_val(r, 'currently', 'precipProbability')),
                'pressure': float(find_val(r, 'currently', 'pressure')),
                'summary': find_val(r, 'currently', 'icon'),
                'precip_max_time': precip_max_time}
        
        return entry

    # Build DataFrame from List of Dictionaries
    def weather_df(self, start_date, end_date):
        list_of_days = date_range(start_date, end_date)

        weather_dicts = []
        for day in list_of_days:
            daily_weather = self.daily_weather(day)
            weather_dicts.append(daily_weather)

        df = pd.DataFrame(weather_dicts)
        df.set_index('date', inplace=True)
        
        # Clean Up NA Values with Forward Fill
        df['apparent_temperature'].fillna(method='ffill',inplace=True)
        df['temperature'].fillna(method='ffill',inplace=True)
        df['humidity'].fillna(method='ffill',inplace=True)
        df['precip_prob'].fillna(method='ffill', inplace=True)
        df['pressure'].fillna(method='ffill', inplace=True)
        df['precip_type'].fillna(value='none', inplace=True)

        return df