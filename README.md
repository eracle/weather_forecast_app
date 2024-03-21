
### Assessment Task for Django Developer
### Weather Forecast App

Tech Stack Required: Django 2 and Rest API
Data source: https://openweathermap.org/api/one-call-api (need to register, key will get
activated in about 1hr after registration)

#### Task Description:
We need to create an application to display the weather forecast for a selected set of
coordinates with selected type of detailing data.

User will require to enter lat and lon in the inputs and chose detailing type according to API
- Current weather
- Minute forecast for 1 hour
- Hourly forecast for 48 hours
- Daily forecast for 7 days

Plus points for: Allow the user to input the location via a Google map plugin.

By default local DB is empty and we should fill it with data from users’ requests.
We need to create API endpoint which will receive
- lat,
- lon
- detailing type

We will first try to find weather forecast in the local DB, if the required data is not present
then we will request it from openweathermap and save to our local DB.
Also, the data that we store in the local DB should be time sensitive, and it should be
configurable from Django settings (by default 10 minutes). This means if the required data
was received more than 10 minutes ago, we need to request the data again, and in case the
new data received is different from the one stored, we will update it in the local DB.

For example:

1. User requests information for “lat: 33.44179 2 lon: -94.03768 9 and detailing type=Minute
    forecast” at 10:00 AM, as we don’t have this data in local DB, we will request data from
    openweathermap and save to the local DB.
2. After 5 minutes, the user again makes the same request (at 10:05). Here we will return
    data from the local DB, because the data is still relevant.
3. Then the user again makes the request after 20 minutes (at 10:25). Here we should
    request data from openweathermap again because the data in the local DB is no longer
    relevant.


Plus points for: Unit and Integration Tests


## Install:
Install make, docker and docker-compose. Then run:
```console
make up
```
Then go to http://0.0.0.0:3000/

### Tests:
Once built, run:
```console
make test
```


# Project Overview

This application leverages the robust foundation provided by the Cookiecutter Django template to create a Django-based weather forecast application, ready for both local development and production deployment. Utilizing Docker for containerization, it simplifies the development and deployment processes while maintaining consistency across different stages of the development lifecycle.

## Project Setup

The project is containerized using Docker, separating configurations for local development and production to ensure environmental consistency:

- **Local Development (`compose/local`):** Includes Dockerfiles for Django and Node.js, catering to backend and frontend development needs.
- **Production (`compose/production`):** Contains Docker configurations optimized for deployment, including Django, Nginx, Postgres, and Traefik for reverse proxy and load balancing.

## Django Configuration

Django app settings are organized into base (`config/settings/base.py`), local (`config/settings/local.py`), and production (`config/settings/production.py`) configurations, allowing for environment-specific customizations.

## Weather Forecast Functionality

Implemented in the `weather` app within the `weather_forecast_app` directory, the core functionality enables fetching weather forecasts based on user-specified coordinates and detail level:

- **Models (`weather/models.py`):** Defines the `WeatherForecast` model to store weather data.
- **API Views (`weather/api/views.py`):** Manages requests to fetch weather forecasts, utilizing local database data or fetching from OpenWeatherMap as necessary.
- **Clients (`weather/clients.py`):** Handles interactions with external weather APIs.

## Frontend Integration

The frontend, developed with React, allows users to select locations on a map and specify the detail level for the weather forecast. The app is bundled using Webpack, with configurations located in the `webpack` directory.

- **React App Entry (`weather_forecast_app/static/js/components/App/App.js`):** Main React component for the application.
- **Webpack Configurations (`webpack/`):** Includes files for bundling and optimizing frontend assets for different environments.

## Testing

A comprehensive test suite covers models, views, and integration points, ensuring backend functionality and potential integration with React component tests.

- **Django Tests (`weather_forecast_app/weather/tests/`):** Includes tests for Django models, views, and utility functions.

## Documentation and Further Reading

- **README.md:** Offers an overview of project setup, including starting the development environment, running tests, and deploying the project.


