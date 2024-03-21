import logging

import pytest
from django.urls import resolve, reverse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_weather_forecast_reverse():
    try:
        url = reverse("weather:forecast")
        assert url == "/weather/forecast/", f"Expected '/weather/forecast/', got '{url}'"
    except Exception as e:
        logger.error(f"Error reversing weather:forecast URL: {e}")
        raise  # Re-raise the exception to fail the test and provide error details to the test runner.


@pytest.mark.django_db
def test_weather_forecast_resolve():
    try:
        match = resolve("/weather/forecast/")
        assert match.view_name == "weather:forecast", f"Expected view name 'weather:forecast', got '{match.view_name}'"
    except Exception as e:
        logger.error(f"Error resolving '/weather/forecast/' URL: {e}")
        raise  # Re-raise the exception to fail the test and provide error details to the test runner.
