from weather_api import WeatherAPI
from dotenv import load_dotenv

def print_weather(weather):
    """
    Prints weather information with emojis and formatted layout
    """
    emoji_map = {
        'clear': '☀️',
        'cloud': '☁️',
        'rain': '🌧️',
        'thunderstorm': '⛈️',
        'snow': '❄️',
        'mist': '🌫️',
        'haze': '🌫️',
        'drizzle': '🌦️'
    }
    
    # Find matching emoji
    condition = next(
        (key for key in emoji_map if key in weather['description'].lower()),
        '🌈'  # Default emoji
    )
    
    print(f"""
{emoji_map.get(condition, '🌤️')} WEATHER REPORT {emoji_map.get(condition, '🌤️')}
{"-" * 35}
📍 Location:    {weather['city']}, {weather['country']}
🌡️ Temperature: {weather['temperature']}°C (Feels {weather['feels_like']}°C)
💧 Humidity:    {weather['humidity']}%
🌬️ Wind:        {weather['wind_speed']} m/s ({weather['wind_deg']}°)
📊 Pressure:    {weather['pressure']} hPa
🌫️ Visibility:  {weather['visibility']/1000:.1f} km
☁️  Cloudiness: {weather['cloudiness']}%
📝 Description: {weather['description'].title()}
""")

if __name__ == "__main__":
    load_dotenv()  # Load environment variables
    
    try:
        # Initialize weather API
        weather_api = WeatherAPI()
        
        # Get city name from user input
        city = input("Please enter the city name: ")
        
        # Get weather data for the entered city
        city_weather = weather_api.get_weather(city)
        
        # Display formatted weather report
        print_weather(city_weather)
        
    except Exception as error:
        print(f"""
⚠️⚠️⚠️ WEATHER REPORT FAILED ⚠️⚠️⚠️
{"-" * 35}
Error: {str(error)}
        
Possible fixes:
1. Check internet connection
2. Verify API key in .env file
3. Try again in 5 minutes
4. Contact support if problem persists
""")