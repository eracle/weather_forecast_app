from django.contrib.gis.db import models as geomodels
from django.db import models
from django.utils import dateformat


class WeatherForecast(models.Model):
    """
    Model to store weather forecast data along with the request parameters and timestamp.
    """
    # Defining detailing types as choices
    CURRENT = 'current'
    MINUTE = 'minute'
    HOURLY = 'hourly'
    DAILY = 'daily'
    DETAILING_CHOICES = [
        (CURRENT, 'Current weather'),
        (MINUTE, 'Minute forecast for 1 hour'),
        (HOURLY, 'Hourly forecast for 48 hours'),
        (DAILY, 'Daily forecast for 7 days'),
    ]

    # For simple latitude and longitude storage, FloatFields could suffice, but using GeoDjango
    # opens up a lot of possibilities for spatial queries if your application scope expands.
    location = geomodels.PointField(help_text="Latitude and longitude of the forecast request.")

    detailing = models.CharField(max_length=10, choices=DETAILING_CHOICES,
                                 help_text="Type of detailing for the weather data.")

    # JSONField can be used to store the weather data fetched from the OpenWeather API.
    # This field allows you to store the weather data in its JSON format directly in the database.
    weather_data = models.JSONField(help_text="The weather forecast data in JSON format.")

    # Timestamp for when the data was last fetched or updated.
    last_updated = models.DateTimeField(help_text="The timestamp when this forecast was last updated.")

    class Meta:
        # Ensures each combination of location and detailing is unique.
        unique_together = ('location', 'detailing')

        # Optimize indexing for the fields you'll query the most.
        indexes = [
            # An index on 'location' and 'detailing' supports efficient retrieval based on these fields.
            models.Index(fields=['location', 'detailing']),
        ]

    def __str__(self):
        # Format 'last_updated' datetime in a more human-readable format
        formatted_last_updated = dateformat.format(self.last_updated, 'N j, Y, P')  # e.g., 'March 15, 2023, 2:30 p.m.'
        return f"Weather data for {self.location} - {self.detailing}, last updated on {formatted_last_updated}"
