# Multi-Line Template & File Upload Guide

## Overview

You can now create templates in three ways:
1. **Interactive multi-line input** - Paste complex templates directly
2. **File upload** - Upload templates from .txt or .md files
3. **PDF upload** - Extract templates from PDF documents

## Method 1: Interactive Template Creator (Recommended for Multi-Line)

### Quick Start

```bash
python create_template.py
```

This launches an interactive menu where you can paste multi-line templates!

### Example Usage

```
📝 Interactive Template Creator

Template name: daily_weather_forecast
Description (optional): Daily weather forecast report

📋 Enter your template content below.
   Press Ctrl+D (Mac/Linux) or Ctrl+Z then Enter (Windows) when done
   OR type 'END' on a new line
----------------------------------------------------------------------
```

**Now paste your template:**

```
Daily Weather Forecast Report
Daily Weather Forecast for {location}, {country}

Current Conditions:
- Temperature: {temperature}°F
- Conditions: {conditions}
- Wind: {wind_speed} mph
- Humidity: {humidity}%

Today's Forecast:
- High: {temperature}°F
- Low: {feels_like}°F
- Conditions: {conditions}
- Precipitation: {precipitation} mm

END
```

Press **Ctrl+D** (or type **END**), then confirm to save!

## Method 2: Upload from Text File

### Step 1: Create a template file

Create `my_template.txt`:
```
Daily Weather Forecast Report
Daily Weather Forecast for {location}, {country}

Current Conditions:
Temperature: {temperature}°F (feels like {feels_like}°F)
Conditions: {conditions}
Wind: {wind_speed} mph
Humidity: {humidity}%
Precipitation: {precipitation} mm

Weather Alerts: [Check local weather service]
```

### Step 2: Upload via Agent

```bash
python starter.py
```

Then:
```
You: Upload template from file called daily_forecast from my_template.txt
```

Or use the interactive tool:
```bash
python create_template.py
# Choose option 2: Create template from file
```

## Method 3: Upload from PDF

### Requirements

Install PyPDF2:
```bash
pip install PyPDF2
```

### Usage via Agent

```
You: Upload template from PDF called weather_template from /path/to/template.pdf
```

### Usage via Interactive Tool

```bash
python create_template.py
# Choose option 2: Create template from file
# Enter PDF path when prompted
```

## Example: Your Daily Weather Forecast Template

Here's how to create the template you specified:

### Option A: Using Interactive Creator

```bash
python create_template.py
```

1. Choose option **1** (Interactive)
2. Name: `daily_forecast_full`
3. Description: `Complete daily weather forecast with 7-day outlook`
4. Paste this template:

```
Daily Weather Forecast Report
Daily Weather Forecast for {location}, {country}

Current Conditions:
- Temperature: {temperature}°F
- Conditions: {conditions}
- Wind: {wind_speed} mph
- Humidity: {humidity}%
- Visibility: Available

Today's Forecast:
- High: {temperature}°F
- Low: {feels_like}°F
- Conditions: {conditions}
- Precipitation Chance: {precipitation} mm
- Wind: {wind_speed} mph

Tonight's Forecast:
- Low: {feels_like}°F
- Conditions: {conditions}
- Wind: {wind_speed} mph

Extended Forecast (Next 7 Days):
[Note: Single location data - for 7-day forecast, call API multiple times]

Weather Alerts: [Check with local weather service]
END
```

5. Press **Ctrl+D** or type **END**
6. Confirm with **y**

### Option B: Save as File First

1. Create `weather_forecast_template.txt` with your template
2. Run `python create_template.py`
3. Choose option **2** (From file)
4. Enter template name and file path

## Available Placeholders for Weather Templates

Use these placeholders in your templates:

- `{location}` - City name
- `{country}` - Country name
- `{temperature}` - Current temperature in °F
- `{feels_like}` - Feels-like temperature in °F
- `{conditions}` - Weather conditions (Clear sky, Rainy, etc.)
- `{humidity}` - Humidity percentage
- `{wind_speed}` - Wind speed in mph
- `{precipitation}` - Precipitation in mm

## Important Notes

### ⚠️ Single Braces Only!

```
✅ CORRECT: {variable}
❌ WRONG: {{variable}}
```

Double braces will cause errors. The system now validates and rejects them.

### 📝 Multi-Line Formatting

Your template preserves:
- Line breaks
- Indentation
- Special characters
- Emojis

### 🔄 Updating Templates

If you need to update a template:

```bash
python starter.py
```

```
You: Update daily_forecast_full template with: [paste new template]
```

Or delete and recreate:
```
You: Delete daily_forecast_full template
# Then create again
```

## Features

### ✅ Supported

- Multi-line templates
- File uploads (.txt, .md, etc.)
- PDF uploads (requires PyPDF2)
- Unicode characters
- Emojis
- Indentation
- Line breaks

### ❌ Not Supported

- Double braces `{{` or `}}`
- Empty placeholders `{}`
- Placeholders with spaces `{my variable}`
- Special characters in placeholders `{temp!}`

## Quick Reference

| Task | Command |
|------|---------|
| Interactive creator | `python create_template.py` |
| Run agent | `python starter.py` |
| List templates | In agent: "List all templates" |
| View template | In agent: "View template daily_forecast" |
| Use template | In agent: "Get NYC weather with daily_forecast template" |

## Troubleshooting

### Issue: "Double braces" error

**Fix:** Use `{variable}` not `{{variable}}`

### Issue: Can't paste multi-line text in agent

**Fix:** Use `python create_template.py` instead

### Issue: PDF extraction fails

**Fix:**
```bash
pip install PyPDF2
```

### Issue: Template not found

**Fix:** Run `python create_template.py` → Option 3 to list all templates

## Advanced: Programmatic Upload

```python
from template_agent import template_agent

# Multi-line template
template = """
Line 1: {placeholder1}
Line 2: {placeholder2}
Line 3: {placeholder3}
"""

template_agent.upload_template("my_template", template, "Description")
```

## Best Practices

1. **Test your template first** - Create with sample data
2. **Use descriptive names** - `daily_forecast_detailed` not `template1`
3. **Add descriptions** - Helps remember what it's for
4. **Keep placeholders simple** - `{temperature}` not `{temp_in_fahrenheit_today}`
5. **Save important templates** - Back up `templates/templates.json`

---

**Ready to create your template?** Run `python create_template.py` and start pasting! 📋
