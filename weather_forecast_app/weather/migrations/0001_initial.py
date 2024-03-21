# Generated by Django 4.2.11 on 2024-03-21 15:41

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(help_text='Latitude and longitude of the forecast request.', srid=4326)),
                ('detailing', models.CharField(choices=[('current', 'Current weather'), ('minute', 'Minute forecast for 1 hour'), ('hourly', 'Hourly forecast for 48 hours'), ('daily', 'Daily forecast for 7 days')], help_text='Type of detailing for the weather data.', max_length=10)),
                ('weather_data', models.JSONField(help_text='The weather forecast data in JSON format.')),
                ('last_updated', models.DateTimeField(help_text='The timestamp when this forecast was last updated.')),
            ],
            options={
                'indexes': [models.Index(fields=['location', 'detailing'], name='weather_wea_locatio_b8ff89_idx')],
                'unique_together': {('location', 'detailing')},
            },
        ),
    ]
