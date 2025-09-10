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

def get_7day_overview():
    """
    Function to fetch and return 7-day overview data for Ratnapura.
    Includes 3 days of historical data, current day's data, and 3 days of forecast.
    Returns a list of dictionaries with date, max temp, min temp, and condition.
    """
    try:
        # Get current weather for the middle day
        current_weather = get_current_weather()
        if not current_weather:
            raise Exception("Failed to fetch current weather")
        today = datetime.now().strftime('%Y-%m-%d')
        current_entry = {
            'date': today,
            'day_of_week': datetime.strptime(today, '%Y-%m-%d').strftime('%A'),
            'max_temp_c': current_weather['temperature_c'],  # Using current temp as max for simplicity
            'min_temp_c': current_weather['temperature_c'],  # Using current temp as min for simplicity
            'condition': current_weather['condition'],
            'precip_mm': 0.0  # Placeholder, as current data doesn't provide daily precip
        }

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
                'precip_mm': history_day['day']['totalprecip_mm']
            }
            history_list.append(entry)
        history_list.reverse()  # Show from oldest to most recent

        # Fetch 3 days of forecast data (including today)
        data = fetch_api('forecast', {'days': 3})
        forecast_days = data['forecast']['forecastday']
        forecast_list = []
        for day in forecast_days[1:4]:  # Start from next day to get 3 days after current
            entry = {
                'date': day['date'],
                'day_of_week': datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A'),
                'max_temp_c': day['day']['maxtemp_c'],
                'min_temp_c': day['day']['mintemp_c'],
                'condition': day['day']['condition']['text'],
                'precip_mm': day['day']['totalprecip_mm']
            }
            forecast_list.append(entry)

        # Combine history, current, and forecast
        overview_list = history_list + [current_entry] + forecast_list
        if FLASK_AVAILABLE:
            current_app.logger.info(f"7-Day Overview: {json.dumps(overview_list, indent=2)}")
        else:
            print(f"7-Day Overview: {json.dumps(overview_list, indent=2)}")
        return overview_list
    except Exception as e:
        if FLASK_AVAILABLE:
            current_app.logger.error(f"Error fetching 7-day overview: {str(e)}")
        else:
            print(f"Error fetching 7-day overview: {str(e)}")
        return []