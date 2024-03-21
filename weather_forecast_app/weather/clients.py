import logging

import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_weather_data(api_key, lat, lon, exclude_parts=None, units='metric', lang='en'):
    """
    Fetches weather data using OpenWeather One Call API 3.0.

    Parameters:
    - api_key (str): Your OpenWeather API key.
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.
    - exclude_parts (list of str, optional): Parts to exclude (current, minutely, hourly, daily, alerts).
    - units (str, optional): Units of measurement ('standard', 'metric', 'imperial').
    - lang (str, optional): Language for the output.

    Returns:
    - dict: The weather data as a dictionary.
    """
    BASE_URL = 'https://openweathermap.org/data/2.5/onecall'
    exclude = ','.join(exclude_parts) if exclude_parts else ''

    params = {
        'appid': api_key,
        'lat': lat,
        'lon': lon,
        'units': units,
        'lang': lang,
    }
    if exclude:
        params['exclude'] = exclude
    response = requests.get(BASE_URL, params=params)

    response.raise_for_status()  # Raises an HTTPError for bad responses

    return response.json()
