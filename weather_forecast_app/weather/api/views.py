from datetime import timedelta

from django.conf import settings
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods

from ..models import WeatherForecast
from ..clients import fetch_weather_data


@require_http_methods(["GET"])
def weather_forecast(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    detailing = request.GET.get('detailing')

    if not (lat and lon and detailing):
        return JsonResponse({'error': 'Missing required parameters.'}, status=400)

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return JsonResponse({'error': 'Invalid latitude or longitude.'}, status=400)
    # After converting lat and lon to floats
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return JsonResponse({'error': 'Latitude must be between -90 and 90 degrees,'
                                      ' and longitude must be between -180 and 180 degrees.'},
                            status=400)

    location = Point(lon, lat)

    # Now using database query to filter by 'last_updated' directly
    recent_threshold = now() - timedelta(minutes=settings.WEATHER_DATA_FRESHNESS_THRESHOLD)  # default 10 minutes
    forecasts = WeatherForecast.objects.filter(
        location=location,
        detailing=detailing,
        last_updated__gte=recent_threshold
    )

    if forecasts.exists():
        forecast = forecasts.first()
    else:
        # If no recent forecasts are found, fetch new data and create/update the record
        weather_data = fetch_weather_data(settings.OPENWEATHERMAP_API_KEY, lat, lon, detailing)
        forecast, created = WeatherForecast.objects.update_or_create(
            location=location,
            detailing=detailing,
            defaults={'weather_data': weather_data, 'last_updated': now()}
        )

    return JsonResponse(forecast.weather_data)
