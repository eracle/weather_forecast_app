import datetime
import random

from django.contrib.gis.geos import Point
from django.utils import timezone
from factory.django import DjangoModelFactory

from ..models import WeatherForecast


class WeatherForecastFactory(DjangoModelFactory):
    class Meta:
        model = WeatherForecast
        django_get_or_create = ['location', 'detailing']

    location = Point(random.uniform(-180, 180), random.uniform(-90, 90))
    detailing = random.choice([choice[0] for choice in WeatherForecast.DETAILING_CHOICES])
    weather_data = {'temperature': random.uniform(0, 40), 'description': 'Sunny with a chance of showers.'}
    last_updated = timezone.now() - datetime.timedelta(days=random.randint(0, 30))
