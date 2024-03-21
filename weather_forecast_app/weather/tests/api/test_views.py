import json
from datetime import timedelta

import pytest
from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils.timezone import now
from rest_framework.test import APIRequestFactory

from weather_forecast_app.weather.api.views import weather_forecast
from ..factories import WeatherForecastFactory
from ...models import WeatherForecast


@pytest.fixture()
def api_rf() -> APIRequestFactory:
    return APIRequestFactory()


@pytest.mark.django_db
class TestWeatherForecastView:
    def test_weather_forecast_with_recent_data_no_api_call(self, api_rf: APIRequestFactory, mocker):
        # Define lat and lon as strings first to ensure exact match with request
        lat_str = '40.75872069597532'
        lon_str = '-73.98529171943665'

        # Convert string representations to float for creating the Point
        lat = float(lat_str)
        lon = float(lon_str)

        # Prepopulate the database with a recent weather forecast
        WeatherForecastFactory(
            location=Point(lon, lat),  # Use floats here for Point creation
            detailing='current',
            weather_data={'temp': 20, 'description': 'Sunny'},
            last_updated=now()
        )

        # Mock the fetch_weather_data function to ensure no API calls are made
        mock_fetch_weather_data = mocker.patch('weather_forecast_app.weather.api.views.fetch_weather_data')

        # Simulate a GET request using the same string representations for lat and lon
        request = api_rf.get('/weather/forecast/', {'lat': lat_str, 'lon': lon_str, 'detailing': 'current'})
        response = weather_forecast(request)

        # Parse the JsonResponse content back into Python data structure
        response_data = json.loads(response.content)

        # Now assert the response data as usual
        assert response.status_code == 200
        assert response_data == {'temp': 20, 'description': 'Sunny'}

        # Verify that fetch_weather_data was not called
        mock_fetch_weather_data.assert_not_called()

    def test_weather_forecast_fetch_new_data(self, api_rf: APIRequestFactory, mocker):
        # Mock the fetch_weather_data function to return a predefined response
        mocked_fetch = mocker.patch(
            'weather_forecast_app.weather.api.views.fetch_weather_data',
            return_value={'temp': 10, 'description': 'Cloudy'}
        )

        # Simulate a GET request for a location with no recent data
        request = api_rf.get('/weather/forecast/', {'lat': '35.6895', 'lon': '139.6917', 'detailing': 'current'})
        response = weather_forecast(request)

        # Verify that fetch_weather_data was called exactly once
        mocked_fetch.assert_called_once()

        # Parse the JsonResponse content back into Python data structure
        response_data = json.loads(response.content)

        # Assert that the parsed response data matches the mocked weather data
        assert response.status_code == 200
        assert response_data == {'temp': 10, 'description': 'Cloudy'}

    def test_weather_forecast_updates_outdated_data(self, api_rf: APIRequestFactory, mocker):
        lat_str = '48.8566'
        lon_str = '2.3522'
        lat = float(lat_str)
        lon = float(lon_str)

        # Create a WeatherForecast object with outdated data
        outdated_last_updated = now() - timedelta(
            minutes=settings.WEATHER_DATA_FRESHNESS_THRESHOLD + 20)  # 5 mins past the threshold
        WeatherForecastFactory(
            location=Point(lon, lat),
            detailing='current',
            weather_data={'temp': 15, 'description': 'Partly cloudy'},
            last_updated=outdated_last_updated
        )
        assert WeatherForecast.objects.count() == 1

        # Mock the fetch_weather_data function to return updated weather data
        new_weather_data = {'temp': 18, 'description': 'Sunny'}
        mocked_fetch = mocker.patch(
            'weather_forecast_app.weather.api.views.fetch_weather_data',
            return_value=new_weather_data
        )

        # Simulate a GET request for the same location and detailing
        request = api_rf.get('/weather/forecast/', {'lat': lat_str, 'lon': lon_str, 'detailing': 'current'})
        response = weather_forecast(request)

        # Verify that fetch_weather_data was called exactly once
        mocked_fetch.assert_called_once()

        # Parse the JsonResponse content back into Python data structure
        response_data = json.loads(response.content)

        # Assert the response matches the new, updated weather data
        assert response.status_code == 200
        assert response_data == new_weather_data

        # Verify the database has been updated with the new weather data
        updated_forecast = WeatherForecast.objects.get(location=Point(lon, lat), detailing='current')
        assert updated_forecast.weather_data == new_weather_data
        assert updated_forecast.last_updated > outdated_last_updated  # Ensure the last_updated field was updated

