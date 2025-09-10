import requests
import json
from datetime import datetime, timedelta
try:
    from flask import current_app
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

API_KEY = 'ee4046c156c4403db3f172241250107'
BASE_URL = 'http://api.weatherapi.com/v1'
LOCATION = 'Ratnapura'

def fetch_api(endpoint, params):
    """
    Helper function to make API requests to WeatherAPI.
    """
    params['key'] = API_KEY
    params['q'] = LOCATION
    response = requests.get(f"{BASE_URL}/{endpoint}.json", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

def get_current_weather():
    """
    Function to fetch and return current weather data for Ratnapura.
    Returns a dictionary with temperature, condition, UV index, and location.
    """
    try:
        data = fetch_api('current', {})
        current = data['current']
        location = data['location']
        result = {
            'temperature_c': current['temp_c'],
            'condition': current['condition']['text'],
            'description': 'Heavy rain, strong winds, and occasional lightning expected. Sudden downpours may lead to localized flooding in some areas.',
            'uv': current['uv'],
            'location': location['name']
        }
        if FLASK_AVAILABLE:
            current_app.logger.info(f"Current Weather: {json.dumps(result, indent=2)}")
        else:
            print(f"Current Weather: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        if FLASK_AVAILABLE:
            current_app.logger.error(f"Error fetching current weather: {str(e)}")
        else:
            print(f"Error fetching current weather: {str(e)}")
        return None

def get_wind():
    """
    Function to fetch wind status for Ratnapura.
    Returns a dictionary with wind speed.
    """
    try:
        data = fetch_api('current', {})
        current = data['current']
        result = {
            'wind_kph': current['wind_kph']
        }
        if FLASK_AVAILABLE:
            current_app.logger.info(f"Wind: {json.dumps(result, indent=2)}")
        else:
            print(f"Wind: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        if FLASK_AVAILABLE:
            current_app.logger.error(f"Error fetching wind: {str(e)}")
        else:
            print(f"Error fetching wind: {str(e)}")
        return None

def get_astronomy():
    """
    Function to fetch sunrise and sunset times for Ratnapura.
    Returns a dictionary with sunrise and sunset times.
    """
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        data = fetch_api('astronomy', {'dt': today})
        astro = data['astronomy']['astro']
        result = {
            'sunrise': astro['sunrise'],
            'sunset': astro['sunset']
        }
        if FLASK_AVAILABLE:
            current_app.logger.info(f"Astronomy: {json.dumps(result, indent=2)}")
        else:
            print(f"Astronomy: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        if FLASK_AVAILABLE:
            current_app.logger.error(f"Error fetching astronomy: {str(e)}")
        else:
            print(f"Error fetching astronomy: {str(e)}")
        return None

def get_timestamp():
    """
    Function to fetch and return the current date and time.
    Returns a dictionary with the formatted date and time.
    """
    try:
        current_time = datetime.now().strftime('%d %b | %H:%M')
        result = {
            'datetime': current_time
        }
        if FLASK_AVAILABLE:
            current_app.logger.info(f"Timestamp: {json.dumps(result, indent=2)}")
        else:
            print(f"Timestamp: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        if FLASK_AVAILABLE:
            current_app.logger.error(f"Error fetching timestamp: {str(e)}")
        else:
            print(f"Error fetching timestamp: {str(e)}")
        return None

def get_weather_background_video(weather_condition):
    """
    Function to determine the appropriate background video based on weather condition.
    Returns the video filename for the current weather condition.
    """
    if not weather_condition:
        if FLASK_AVAILABLE:
            current_app.logger.info("No weather condition provided, using default video: videos/bg_vdo02.mp4")
        else:
            print("No weather condition provided, using default video: videos/bg_vdo02.mp4")
        return 'videos/bg_vdo02.mp4'  # Default video
    
    condition = weather_condition.lower()
    if FLASK_AVAILABLE:
        current_app.logger.info(f"Weather condition: '{condition}'")
    else:
        print(f"Weather condition: '{condition}'")
    
    # Clear conditions
    if condition in ['clear']:
        return 'videos/weather/sunny.mp4'
    
    # Partly Cloudy conditions
    elif condition in ['partly cloudy']:
        if FLASK_AVAILABLE:
            current_app.logger.info("Partly cloudy condition detected, using videos/bg_vdo02.mp4")
        else:
            print("Partly cloudy condition detected, using videos/bg_vdo02.mp4")
        return 'videos/bg_vdo02.mp4'  # Fallback until partly_cloudy.mp4 is added
    
    # Cloudy conditions
    elif condition in ['cloudy']:
        return 'videos/bg_vdo02.mp4'  # Fallback until cloudy.mp4 is added
    
    # Overcast conditions
    elif condition in ['overcast']:
        return 'videos/bg_vdo02.mp4'  # Fallback until overcast.mp4 is added
    
    # Mist conditions
    elif condition in ['mist']:
        return 'videos/bg_vdo02.mp4'  # Fallback until mist.mp4 is added
    
    # Patchy Rain Possible
    elif condition in ['patchy rain possible']:
        return 'videos/weather/patchy_rain.mp4'  # This video exists
    
    # Patchy Light Drizzle
    elif condition in ['patchy light drizzle']:
        return 'videos/bg_vdo03.mp4'  # Fallback until patchy_light_drizzle.mp4 is added
    
    # Light Drizzle
    elif condition in ['light drizzle']:
        return 'videos/bg_vdo03.mp4'  # Fallback until light_drizzle.mp4 is added
    
    # Patchy Light Rain
    elif condition in ['patchy light rain']:
        return 'videos/bg_vdo03.mp4'  # Fallback until patchy_light_rain.mp4 is added
    
    # Light Rain
    elif condition in ['light rain']:
        return 'videos/bg_vdo03.mp4'  # Fallback until light_rain.mp4 is added
    
    # Moderate Rain at Times
    elif condition in ['moderate rain at times']:
        return 'videos/bg_vdo03.mp4'  # Fallback until moderate_rain_at_times.mp4 is added
    
    # Moderate Rain
    elif condition in ['moderate rain']:
        return 'videos/bg_vdo03.mp4'  # Fallback until moderate_rain.mp4 is added
    
    # Heavy Rain at Times
    elif condition in ['heavy rain at times']:
        return 'videos/bg_vdo03.mp4'  # Fallback until heavy_rain_at_times.mp4 is added
    
    # Heavy Rain
    elif condition in ['heavy rain']:
        return 'videos/bg_vdo03.mp4'  # Fallback until heavy_rain.mp4 is added
    
    # Light Rain Shower
    elif condition in ['light rain shower']:
        return 'videos/bg_vdo03.mp4'  # Fallback until light_rain_shower.mp4 is added
    
    # Moderate or Heavy Rain Shower
    elif condition in ['moderate or heavy rain shower']:
        return 'videos/bg_vdo03.mp4'  # Fallback until moderate_heavy_rain_shower.mp4 is added
    
    # Torrential Rain Shower
    elif condition in ['torrential rain shower']:
        return 'videos/bg_vdo03.mp4'  # Fallback until torrential_rain_shower.mp4 is added
    
    # Patchy Light Rain with Thunder
    elif condition in ['patchy light rain with thunder']:
        return 'videos/weather/thunderstorm.mp4'  # This video exists
    
    # Moderate or Heavy Rain with Thunder
    elif condition in ['moderate or heavy rain with thunder']:
        return 'videos/weather/thunderstorm.mp4'  # This video exists
    
    # Fallback patterns for similar conditions
    elif any(word in condition for word in ['thunder', 'thunderstorm']):
        return 'videos/weather/thunderstorm.mp4'
    
    elif any(word in condition for word in ['rain', 'drizzle', 'shower']):
        return 'videos/weather/patchy_rain.mp4'
    
    elif any(word in condition for word in ['cloudy', 'overcast']):
        return 'videos/bg_vdo02.mp4'
    
    elif any(word in condition for word in ['mist', 'fog']):
        return 'videos/bg_vdo02.mp4'
    
    # Default fallback
    else:
        return 'videos/bg_vdo02.mp4'

def get_weather_icon(weather_condition):
    """
    Function to map weather conditions to FontAwesome icons.
    Returns the appropriate icon class for the weather condition.
    """
    if not weather_condition:
        return 'fas fa-question-circle'  # Default icon
    
    condition = weather_condition.lower()
    
    # Clear conditions
    if condition in ['clear']:
        return 'fas fa-sun'
    
    # Partly Cloudy conditions
    elif condition in ['partly cloudy']:
        return 'fas fa-cloud-sun'
    
    # Cloudy conditions
    elif condition in ['cloudy']:
        return 'fas fa-cloud'
    
    # Overcast conditions
    elif condition in ['overcast']:
        return 'fas fa-cloud'
    
    # Mist conditions
    elif condition in ['mist']:
        return 'fas fa-smog'
    
    # Rain conditions
    elif any(word in condition for word in ['rain', 'drizzle', 'shower']):
        if 'light' in condition:
            return 'fas fa-cloud-rain'
        elif 'heavy' in condition or 'torrential' in condition:
            return 'fas fa-cloud-showers-heavy'
        else:
            return 'fas fa-cloud-rain'
    
    # Thunderstorm conditions
    elif any(word in condition for word in ['thunder', 'thunderstorm']):
        return 'fas fa-bolt'
    
    # Snow conditions
    elif any(word in condition for word in ['snow', 'sleet']):
        return 'fas fa-snowflake'
    
    # Fog conditions
    elif any(word in condition for word in ['fog', 'haze']):
        return 'fas fa-smog'
    
    # Default fallback
    else:
        return 'fas fa-cloud'

def get_7day_overview():
    """
    Function to fetch and return 7-day overview data for Ratnapura.
    Includes 3 days of historical data, current day's data, and 3 days of forecast.
    Returns a list of dictionaries with date, max temp, min temp, and condition.
    """
    try:
        # Fetch 3 days of historical data
        history_list = []
        for i in range(3):
            date = (datetime.now() - timedelta(days=i+1)).strftime('%Y-%m-%d')
            data = fetch_api('history', {'dt': date})
            history_day = data['forecast']['forecastday'][0]
            entry = {
                'date': history_day['date'],
                'day_of_week': datetime.strptime(history_day['date'], '%Y-%m-%d').strftime('%A'),
                'max_temp_c': history_day['day']['maxtemp_c'],
                'min_temp_c': history_day['day']['mintemp_c'],
                'condition': history_day['day']['condition']['text'],
                'icon': get_weather_icon(history_day['day']['condition']['text']),
                'precip_mm': history_day['day']['totalprecip_mm']
            }
            history_list.append(entry)
        history_list.reverse()  # Show from oldest to most recent

        # Fetch 3 days of forecast data (free plan limit: 3 days max)
        data = fetch_api('forecast', {'days': 3})
        forecast_days = data['forecast']['forecastday']
        
        # Get current day (today) from forecast data
        current_day = forecast_days[0]
        current_entry = {
            'date': current_day['date'],
            'day_of_week': datetime.strptime(current_day['date'], '%Y-%m-%d').strftime('%A'),
            'max_temp_c': current_day['day']['maxtemp_c'],
            'min_temp_c': current_day['day']['mintemp_c'],
            'condition': current_day['day']['condition']['text'],
            'icon': get_weather_icon(current_day['day']['condition']['text']),
            'precip_mm': current_day['day']['totalprecip_mm']
        }
        
        # Get 2 days after current day (free plan only allows 3 days total)
        forecast_list = []
        for day in forecast_days[1:3]:  # This gives us tomorrow and day after tomorrow
            entry = {
                'date': day['date'],
                'day_of_week': datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A'),
                'max_temp_c': day['day']['maxtemp_c'],
                'min_temp_c': day['day']['mintemp_c'],
                'condition': day['day']['condition']['text'],
                'icon': get_weather_icon(day['day']['condition']['text']),
                'precip_mm': day['day']['totalprecip_mm']
            }
            forecast_list.append(entry)
        
        # Add a placeholder day to make it 7 days total
        # Since we can't get more forecast data, we'll use current day data as placeholder
        placeholder_day = {
            'date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'day_of_week': (datetime.now() + timedelta(days=3)).strftime('%A'),
            'max_temp_c': current_day['day']['maxtemp_c'],  # Use current day as reference
            'min_temp_c': current_day['day']['mintemp_c'],
            'condition': current_day['day']['condition']['text'],
            'icon': get_weather_icon(current_day['day']['condition']['text']),
            'precip_mm': 0.0
        }
        forecast_list.append(placeholder_day)

        # Combine history, current, and forecast
        overview_list = history_list + [current_entry] + forecast_list
        
        # Debug: Check the count
        if FLASK_AVAILABLE:
            current_app.logger.info(f"7-Day Overview - History: {len(history_list)}, Current: 1, Forecast: {len(forecast_list)}, Total: {len(overview_list)}")
            current_app.logger.info(f"7-Day Overview: {json.dumps(overview_list, indent=2)}")
        else:
            print(f"7-Day Overview - History: {len(history_list)}, Current: 1, Forecast: {len(forecast_list)}, Total: {len(overview_list)}")
            print(f"7-Day Overview: {json.dumps(overview_list, indent=2)}")
        return overview_list
    except Exception as e:
        if FLASK_AVAILABLE:
            current_app.logger.error(f"Error fetching 7-day overview: {str(e)}")
        else:
            print(f"Error fetching 7-day overview: {str(e)}")
        return []