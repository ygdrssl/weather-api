import requests
import os

class WeatherAPI:
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Get one from OpenWeatherMap")

    def get_weather(self, city, country_code=None, units='metric'):
        """
        Get current weather data for a city
        Args:
            city (str): City name
            country_code (str): Optional country code (e.g., 'US')
            units (str): Temperature units (metric, imperial, or standard)
        Returns:
            dict: Weather data
        """
        params = {
            'q': f"{city},{country_code}" if country_code else city,
            'units': units,
            'appid': self.api_key
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return self._parse_weather_data(data)
        except requests.exceptions.HTTPError as err:
            if response.status_code == 401:
                raise ValueError("Invalid API key") from err
            if response.status_code == 404:
                raise ValueError("City not found") from err
            raise
        except requests.exceptions.RequestException as err:
            raise ConnectionError(f"Connection error: {err}") from err

    def _parse_weather_data(self, data):
        """Parse raw API response into standardized format"""
        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind'].get('deg', None),
            'description': data['weather'][0]['description'],
            'visibility': data.get('visibility', None),
            'cloudiness': data['clouds']['all']
        }

