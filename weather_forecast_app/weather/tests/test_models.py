import pytest

from .factories import WeatherForecastFactory

pytestmark = pytest.mark.django_db


class TestWeatherForecast:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, request):
        self.method_name = request.function.__name__
        self.sut = WeatherForecastFactory()  # sut stands for System Under Test

    def test_sut(self):
        assert self.sut is not None

    @pytest.mark.parametrize(
        "attr_name",
        [
            "location",
            "detailing",
            "weather_data",
            "last_updated",
        ],
        ids=[
            "location",
            "detailing",
            "weather_data",
            "last_updated",
        ],
    )
    def test_is_not_null_(self, attr_name):
        assert getattr(self.sut, attr_name) is not None

    def test_str_representation(self):
        str_representation = str(self.sut)
        assert str_representation
