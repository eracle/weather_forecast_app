from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WeatherConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "weather_forecast_app.weather"
    verbose_name = _("Weather")
