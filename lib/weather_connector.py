import requests
from datetime import datetime
import pytz

UNITS = 'metric'
GOOD = {"Clear", "Clouds"}
MAX_COLD = 12
MIN_HOT = 26

def is_after_5pm_est():
    current_time = datetime.now(pytz.utc)
    est_timezone = pytz.timezone('US/Eastern')
    est_time = current_time.astimezone(est_timezone)

    hour = est_time.hour

    # Check if the hour is greater than or equal to 18 (6 PM)
    if hour >= 18 or hour <= 3:
        return True
    else:
        return False
    

def set_condition(main_weather, id, min_temp, max_temp):
    condition = main_weather
    if main_weather in GOOD:
        condition = "GOOD"
    
    if int(id) >= 700 and int(id) <= 799:
        condition = "Atmoshphere"
    elif min_temp < MAX_COLD:
        condition = "COLD"
    elif max_temp > MIN_HOT:
        condition = "HOT"
    
    return condition



def get_weather_condition(api_key, city):
    geocoding_url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()

    if len(geocoding_data) > 0:
        latitude = geocoding_data[0]['lat']
        longitude = geocoding_data[0]['lon']

        api_url = "onecall"
        is_after_5pm = is_after_5pm_est()

        if is_after_5pm:
            api_url = "forecast"
            
        weather_url = f"https://api.openweathermap.org/data/2.5/{api_url}?lat={latitude}&lon={longitude}&units={UNITS}&appid={api_key}"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if is_after_5pm:
            weather_3_hours = weather_data['list'][0]
            weather_3_hours_type = weather_3_hours["weather"][0]
            print('Weather 3 Hours from Now:', weather_3_hours)
            condition = set_condition(weather_3_hours_type['main'], weather_3_hours_type['id'], weather_3_hours['main']['temp_min'], weather_3_hours['main']['temp_max'])
        else:
            weather_daily = weather_data['daily'][0]
            print(weather_daily)
            weather_daily_type= weather_daily['weather'][0]
            weather_daily_temp = weather_daily['temp']
            condition = set_condition(weather_daily_type['main'], weather_daily_type['id'], weather_daily_temp['min'], weather_daily_temp['max'])

        print(f"condition: {condition}")
        return condition

    else:
        print("City not found. Please try again.")
