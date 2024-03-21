# tests.py or tests/test_openweathermap_api.py
import pytest
from django.conf import settings

from ..clients import fetch_weather_data  # Adjust the import path based on your project structure


@pytest.mark.skip(reason="This test makes a live API call, skip to avoid hitting the API too frequently")
def test_openweathermap_api_call():
    # Example coordinates for New York City
    latitude = '40.7128'
    longitude = '-74.0060'
    api_key = settings.OPENWEATHERMAP_API_KEY

    weather_data = fetch_weather_data(api_key, latitude, longitude)
    # print(weather_data)  # This will print the weather data to your console

    # Ensure that the 'current' key is in the response, indicating successful data retrieval
    assert 'current' in weather_data, "The API response did not include 'current' weather data"
