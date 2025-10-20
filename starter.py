from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, tool, FinalAnswerTool
import datetime
import requests
import pytz
from smolagents import LiteLLMModel
import json
import os

import yaml

# Import TemplateAgent tools
from template_agent import (
    upload_template,
    list_all_templates,
    view_template_content,
    delete_template,
    generate_from_template,
    update_existing_template,
    upload_template_from_file,
    upload_template_from_pdf
)

# TemplateAgent is imported above and handles all template management


@tool
def get_weather(location: str) -> dict:
    """Fetches current weather information for a specified location using the Open-Meteo API (no API key needed).

    Args:
        location: The city name or location (e.g., 'New York', 'London', 'Tokyo')

    Returns:
        A dictionary containing weather information with keys: location, country, temperature, feels_like, conditions, humidity, wind_speed, precipitation
    """
    try:
        # First, geocode the location using Open-Meteo's geocoding API
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        geo_response = requests.get(geocode_url)
        geo_data = geo_response.json()

        if not geo_data.get('results'):
            return {"error": f"Could not find location: {location}. Please check the spelling and try again."}

        # Get coordinates
        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']
        location_name = geo_data['results'][0]['name']
        country = geo_data['results'][0].get('country', '')

        # Fetch weather data
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&temperature_unit=fahrenheit&wind_speed_unit=mph"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        current = weather_data['current']

        # Weather code interpretation (WMO codes)
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Foggy", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }

        weather_desc = weather_codes.get(current['weather_code'], "Unknown")

        return {
            "location": location_name,
            "country": country,
            "temperature": current['temperature_2m'],
            "feels_like": current['apparent_temperature'],
            "conditions": weather_desc,
            "humidity": current['relative_humidity_2m'],
            "wind_speed": current['wind_speed_10m'],
            "precipitation": current['precipitation']
        }

    except Exception as e:
        return {"error": f"Error fetching weather for '{location}': {str(e)}"}


@tool
def get_weather_with_template(location: str, template_name: str = "default_weather") -> str:
    """LINKED TOOL: Fetches weather data and automatically formats it using a specified template.
    This is the main integration point between weather and template agents.

    Args:
        location: The city name or location (e.g., 'New York', 'London', 'Tokyo')
        template_name: Name of the template to use for formatting (default: 'default_weather')

    Returns:
        Formatted weather report using the specified template

    Example:
        get_weather_with_template("Buffalo", "weather_simple")
    """
    # Step 1: Get weather data
    weather_data = get_weather(location)

    # Step 2: Check for errors
    if isinstance(weather_data, dict) and 'error' in weather_data:
        return weather_data['error']

    # Step 3: Apply template using TemplateAgent
    from template_agent import template_agent
    result = template_agent.generate_content(template_name, weather_data)

    return result


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """Fetches the current local time in a specified timezone.

    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo')

    Returns:
        The current time in the specified timezone.
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


# Initialize the model
model = LiteLLMModel(
        model_id="ollama_chat/qwen3:8b",  # Or try other Ollama-supported models
        api_base="http://127.0.0.1:11434",  # Default Ollama local server
        num_ctx=8192,
    )

# Initialize search tool
search_tool = DuckDuckGoSearchTool()

# Initialize default templates
from template_agent import template_agent

def setup_default_templates():
    """Create default templates if they don't exist."""
    # Default weather template
    if not template_agent.get_template("default_weather"):
        template_agent.upload_template(
            "default_weather",
            """🌤️ Weather Report for {location}, {country}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌡️ Temperature: {temperature}°F (feels like {feels_like}°F)
☁️ Conditions: {conditions}
💧 Humidity: {humidity}%
💨 Wind Speed: {wind_speed} mph
🌧️ Precipitation: {precipitation} mm
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""",
            "Default weather report format"
        )

    # Simple weather template
    if not template_agent.get_template("weather_simple"):
        template_agent.upload_template(
            "weather_simple",
            "{location} is {temperature}°F with {conditions}",
            "Simple one-line weather format"
        )

    # Detailed weather template
    if not template_agent.get_template("weather_detailed"):
        template_agent.upload_template(
            "weather_detailed",
            """Weather Analysis for {location}, {country}
Temperature: {temperature}°F (Feels like: {feels_like}°F)
Current Conditions: {conditions}
Atmospheric Humidity: {humidity}%
Wind Velocity: {wind_speed} mph
Precipitation Level: {precipitation} mm""",
            "Detailed weather analysis format"
        )

setup_default_templates()

# Create the agent with weather tools and TemplateAgent
agent = CodeAgent(
    model=model,
    tools=[
        # Weather tools
        get_weather,
        get_weather_with_template,  # LINKED TOOL - combines weather + template
        get_current_time_in_timezone,
        # TemplateAgent tools - Universal template system
        upload_template,
        upload_template_from_file,
        upload_template_from_pdf,
        list_all_templates,
        view_template_content,
        delete_template,
        generate_from_template,
        update_existing_template
    ],
    max_steps=10,
    verbosity_level=1
)

# Run the agent
if __name__ == "__main__":
    print("=" * 70)
    print("🤖 AI Agent with LINKED Weather + Template System - Ready!")
    print("=" * 70)

    # Show default templates loaded
    print("\n✅ Pre-loaded Templates:")
    print("   • default_weather - Full weather report format")
    print("   • weather_simple - One-line weather format")
    print("   • weather_detailed - Detailed weather analysis")

    print("\n🔗 LINKED AGENT WORKFLOWS:")
    print("   1. Get weather with auto-formatting:")
    print('      "Show Buffalo weather using weather_simple template"')
    print('      "Get NYC weather with the detailed template"')
    print("")
    print("   2. Separate steps (manual control):")
    print('      "Get weather for Paris"')
    print('      "Generate from weather_simple template with that data"')

    print("\n📋 TEMPLATE MANAGEMENT:")
    print("   • Upload new templates")
    print("   • List all templates")
    print("   • View/Update/Delete templates")
    print("   • Works with ANY content type!")

    print("\n🌤️  WEATHER TOOLS:")
    print("   • get_weather(location) - Raw weather data")
    print("   • get_weather_with_template(location, template) - Formatted output")
    print("   • get_current_time_in_timezone(timezone)")

    print("\n💡 QUICK START EXAMPLES:")
    print('   "What\'s the weather in Buffalo?" (uses default template)')
    print('   "Get Tokyo weather with weather_simple template"')
    print('   "List all my templates"')
    print('   "Upload a template named tweet with: 🌤️ {location}: {temperature}°F"')

    print("\n📁 MULTI-LINE TEMPLATES & FILE UPLOAD:")
    print("   • For multi-line templates: run 'python create_template.py'")
    print("   • Paste entire templates (with line breaks!)")
    print("   • Upload from .txt, .md, or .pdf files")
    print('   • Agent: "Upload template from file my_template.txt"')

    print("\n📚 Documentation:")
    print("   • MULTI_LINE_TEMPLATE_GUIDE.md - File upload & multi-line input")
    print("   • TEMPLATE_AGENT_GUIDE.md - Full template system docs")
    print("   • AGENT_LINKING_GUIDE.md - Integration patterns")
    print("   • TROUBLESHOOTING.md - Common issues & fixes")

    print("\nType 'exit' or 'quit' to stop.")
    print("=" * 70)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ['exit', 'quit', 'q']:
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        try:
            result = agent.run(user_input)
            print(f"\nAssistant: {result}")
        except Exception as e:
            print(f"\nError: {str(e)}")