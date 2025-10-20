# Agent Linking Guide: Weather Agent + TemplateAgent

## Overview

This guide explains how the **Weather Agent** and **TemplateAgent** are linked together to create a powerful, flexible content generation system.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CodeAgent (Main)                       │
│                                                             │
│  ┌──────────────────┐           ┌────────────────────┐    │
│  │  Weather Agent   │◄─────────►│  TemplateAgent     │    │
│  │                  │  Linked   │                    │    │
│  │ • get_weather()  │   Tool    │ • upload_template()│    │
│  │ • get_time()     │           │ • generate_from()  │    │
│  └──────────────────┘           └────────────────────┘    │
│           │                              │                 │
│           └──────────┬───────────────────┘                 │
│                      ▼                                     │
│         ┌───────────────────────────┐                     │
│         │ get_weather_with_template()│ ← LINKING FUNCTION │
│         └───────────────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## How They're Linked

### 1. **Direct Link: `get_weather_with_template()`**

This is the main linking function (starter.py:86-111) that:
- Fetches weather data using `get_weather()`
- Automatically applies a template using TemplateAgent
- Returns formatted output

**Code:**
```python
@tool
def get_weather_with_template(location: str, template_name: str = "default_weather") -> str:
    # Step 1: Get weather data
    weather_data = get_weather(location)

    # Step 2: Check for errors
    if isinstance(weather_data, dict) and 'error' in weather_data:
        return weather_data['error']

    # Step 3: Apply template
    result = template_agent.generate_content(template_name, weather_data)

    return result
```

### 2. **Indirect Link: Manual Workflow**

Users can also manually combine the agents:
```
Step 1: weather_data = get_weather("Buffalo")
Step 2: result = generate_from_template("my_template", weather_data)
```

## Three Ways to Use the Linked System

### Method 1: Auto-Linked (Easiest)
Use the `get_weather_with_template()` function:

```
You: Get Buffalo weather with weather_simple template
```

The agent automatically:
1. Calls `get_weather("Buffalo")`
2. Calls `generate_from_template("weather_simple", weather_data)`
3. Returns formatted result

### Method 2: Agent-Driven Workflow
Let the agent figure out the steps:

```
You: Show me Tokyo weather using the detailed template
```

The agent will:
1. Recognize it needs weather data
2. Recognize it needs to format with a template
3. Execute both tools and combine results

### Method 3: Manual Control
You direct each step:

```
You: Get weather for Paris

[Agent returns raw data]

You: Now format that using weather_simple template
```

## Default Templates

Three templates are automatically created on startup:

1. **default_weather** - Full formatted report
2. **weather_simple** - One-line format
3. **weather_detailed** - Analysis format

Location: `templates/templates.json`

## Creating Custom Integrations

### Example: Creating a Twitter Weather Bot Template

```
You: Upload a template named weather_tweet with template:
🌤️ Weather Update: {location}
🌡️ {temperature}°F | {conditions}
💨 Wind: {wind_speed} mph
#weather #{location}

Description: Twitter-friendly weather format
```

Then use it:
```
You: Get NYC weather with weather_tweet template
```

### Example: Creating an Email Weather Alert

```
You: Upload a template named weather_email with template:
Subject: Weather Alert for {location}

Current conditions in {location}, {country}:
Temperature: {temperature}°F (Feels like {feels_like}°F)
Conditions: {conditions}
Humidity: {humidity}%

Stay safe!

Description: Email format for weather alerts
```

## Data Flow

### Weather Data Structure
```python
{
    "location": "Buffalo",
    "country": "United States",
    "temperature": 71.1,
    "feels_like": 66.6,
    "conditions": "Clear sky",
    "humidity": 39,
    "wind_speed": 7.6,
    "precipitation": 0.0
}
```

### Template Placeholders
Templates can use any of these keys:
- `{location}` - City name
- `{country}` - Country name
- `{temperature}` - Temperature in °F
- `{feels_like}` - Feels-like temperature
- `{conditions}` - Weather conditions
- `{humidity}` - Humidity percentage
- `{wind_speed}` - Wind speed in mph
- `{precipitation}` - Precipitation in mm

## Advanced Linking Patterns

### Pattern 1: Conditional Formatting

Create multiple templates for different conditions:
```
- weather_hot: For temp > 80°F
- weather_cold: For temp < 40°F
- weather_rainy: For precipitation > 0
```

The agent can intelligently choose the right template.

### Pattern 2: Multi-Location Comparison

```
You: Compare weather in NYC and LA using weather_simple template
```

The agent will:
1. Get weather for NYC
2. Get weather for LA
3. Format both using the template
4. Present comparison

### Pattern 3: Template Chaining

Create templates that reference other templates:
```
- weather_header: Title template
- weather_body: Data template
- weather_footer: Footer template
```

## Extending to Other Agents

This linking pattern works for ANY data source + template combination:

### News + Template
```python
@tool
def get_news_with_template(topic: str, template_name: str):
    news_data = get_news(topic)
    return template_agent.generate_content(template_name, news_data)
```

### Stock Data + Template
```python
@tool
def get_stock_with_template(symbol: str, template_name: str):
    stock_data = get_stock_price(symbol)
    return template_agent.generate_content(template_name, stock_data)
```

### Calendar + Template
```python
@tool
def get_events_with_template(date: str, template_name: str):
    events_data = get_calendar_events(date)
    return template_agent.generate_content(template_name, events_data)
```

## Best Practices

1. **Use descriptive template names** - `weather_email` not `template1`
2. **Test templates with sample data** before production use
3. **Create templates for common use cases** upfront
4. **Document your templates** with good descriptions
5. **Version your templates** - save backups of `templates/templates.json`

## Troubleshooting

### Issue: Template not found
```
Error: Template 'xyz' not found
```
**Solution:** Run `list all templates` to see available templates

### Issue: Missing placeholder
```
Error: Missing data for placeholder 'abc'
```
**Solution:** Check template placeholders match weather data keys

### Issue: Agent not using template
**Solution:** Explicitly mention the template name in your query

## Performance Tips

1. **Use `get_weather_with_template()`** for single operations (faster)
2. **Use separate calls** when you need to inspect/modify data between steps
3. **Pre-load common templates** on startup (already done for weather)

## Summary

The linking system gives you:
- ✅ **Automatic integration** via `get_weather_with_template()`
- ✅ **Manual control** when needed
- ✅ **Reusable templates** for consistent formatting
- ✅ **Extensible pattern** for any data + template combination

**Key File:** `starter.py:86-111` - The linking function
**Storage:** `templates/templates.json` - Template persistence
**Documentation:** `TEMPLATE_AGENT_GUIDE.md` - Full template docs

---

**Happy linking!** 🔗
