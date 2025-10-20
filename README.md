# AI Weather Agent with TemplateAgent System

A powerful AI agent system that combines weather data fetching with a universal template management system for flexible content generation.

## 🚀 Quick Start

### Option 1: Run the Agent
```bash
python starter.py
```

### Option 2: Create Multi-Line Templates
```bash
python create_template.py
```

## ✨ Features

### 🌤️ Weather Agent
- Fetch current weather for any location (Open-Meteo API - no key needed)
- Get timezone information
- Returns structured data (temperature, conditions, humidity, wind, precipitation)

### 📋 TemplateAgent System
- **Universal template management** for any content type
- **Multi-line template support** - paste complex templates directly
- **File upload** - Upload templates from .txt, .md files
- **PDF upload** - Extract templates from PDF documents
- **Persistent storage** - Templates saved between sessions
- **Validation** - Prevents common template errors

### 🔗 Linked System
- Automatic integration between weather data and templates
- One-command weather reports with custom formatting
- Flexible workflow options (automatic or manual)

## 📖 Usage Examples

### Basic Weather Query
```
You: What's the weather in New York?
```

### Weather with Specific Template
```
You: Get Tokyo weather with weather_simple template
```

### Create Multi-Line Template
```bash
python create_template.py
```
Then paste your template!

### Upload Template from File
```
You: Upload template from file called daily_forecast from example_daily_forecast_template.txt
```

### List Templates
```
You: List all my templates
```

## 📁 Project Structure

```
├── starter.py                          # Main agent entry point
├── create_template.py                  # Interactive template creator
├── template_agent.py                   # TemplateAgent core system
├── templates/                          # Template storage
│   └── templates.json                  # Saved templates
├── example_daily_forecast_template.txt # Example template file
└── Documentation:
    ├── README.md                       # This file
    ├── MULTI_LINE_TEMPLATE_GUIDE.md   # Multi-line & file upload guide
    ├── TEMPLATE_AGENT_GUIDE.md        # Complete template system docs
    ├── AGENT_LINKING_GUIDE.md         # Integration patterns
    └── TROUBLESHOOTING.md             # Common issues & solutions
```

## 🎯 Three Ways to Create Templates

### 1. Direct in Agent (Single Line)
```
You: Upload a template named simple with: {location} is {temperature}°F
```

### 2. Interactive Creator (Multi-Line) ⭐ RECOMMENDED
```bash
python create_template.py
```
- Choose option 1
- Paste your entire template
- Press Ctrl+D or type END

### 3. From File
```
You: Upload template from file my_template from /path/to/template.txt
```

Or:
```bash
python create_template.py
```
- Choose option 2
- Enter file path

## 🔧 Installation

### Requirements
```bash
pip install smolagents requests pytz PyPDF2
```

### Optional (for PDF support)
```bash
pip install PyPDF2
```

## 📚 Available Templates (Pre-loaded)

| Template Name | Description |
|--------------|-------------|
| `default_weather` | Full weather report with emojis |
| `weather_simple` | One-line format |
| `weather_detailed` | Detailed analysis format |
| `daily_weather_forecast` | Daily forecast format |

## 🎨 Template Placeholders

For weather templates, use these placeholders:

- `{location}` - City name
- `{country}` - Country name
- `{temperature}` - Temperature in °F
- `{feels_like}` - Feels-like temperature
- `{conditions}` - Weather conditions
- `{humidity}` - Humidity percentage
- `{wind_speed}` - Wind speed (mph)
- `{precipitation}` - Precipitation (mm)

## 💡 Example Templates

### Simple Format
```
{location} is {temperature}°F with {conditions}
```

### Detailed Format
```
Daily Weather Forecast for {location}, {country}

Current Conditions:
- Temperature: {temperature}°F (feels like {feels_like}°F)
- Conditions: {conditions}
- Humidity: {humidity}%
- Wind: {wind_speed} mph
- Precipitation: {precipitation} mm
```

### Tweet Format
```
🌤️ Weather Update: {location}
🌡️ {temperature}°F | {conditions}
💨 Wind: {wind_speed} mph
#weather #{location}
```

## 🛠️ Configuration

### Model Setup
Edit `starter.py` to change the LLM model:

```python
model = LiteLLMModel(
    model_id="ollama_chat/qwen2:7b",  # Change this
    api_base="http://127.0.0.1:11434",
    num_ctx=8192,
)
```

### Template Storage
Templates are stored in: `templates/templates.json`

Backup this file to save your templates!

## 📖 Documentation

| Guide | Purpose |
|-------|---------|
| **MULTI_LINE_TEMPLATE_GUIDE.md** | How to create multi-line templates and upload files |
| **TEMPLATE_AGENT_GUIDE.md** | Complete TemplateAgent documentation |
| **AGENT_LINKING_GUIDE.md** | How weather and templates are linked |
| **TROUBLESHOOTING.md** | Common errors and solutions |

## 🔍 Common Tasks

### View Template Content
```
You: View template content for daily_weather_forecast
```

### Delete Template
```
You: Delete template weather_simple
```

### Update Template
```
You: Update template daily_forecast with: [new template]
```

## ⚠️ Important Notes

### ✅ DO:
- Use single braces: `{variable}`
- Test templates before production use
- Back up `templates/templates.json`

### ❌ DON'T:
- Use double braces: `{{variable}}`
- Use empty placeholders: `{}`
- Use spaces in names: `{my variable}`

## 🐛 Troubleshooting

### Error: "Single '}' encountered"
**Fix:** Use `{variable}` not `{{variable}}`
See: TROUBLESHOOTING.md

### Can't paste multi-line template
**Fix:** Use `python create_template.py`

### PDF upload fails
**Fix:** `pip install PyPDF2`

## 🎓 Learning Path

1. **Start here:** Run `python starter.py` and try basic weather queries
2. **Create templates:** Use `python create_template.py` to make your first template
3. **Read docs:** Check MULTI_LINE_TEMPLATE_GUIDE.md
4. **Advanced:** Read AGENT_LINKING_GUIDE.md for integration patterns

## 🤝 Contributing

This is a demo/educational project. Feel free to extend it!

### Ideas for Extension
- Add more data sources (news, stocks, etc.)
- Create template categories
- Add template versioning
- Build a web interface
- Add more weather data (forecasts, historical)

## 📄 License

Educational/Demo Project

## 🙏 Acknowledgments

- Uses [Open-Meteo API](https://open-meteo.com/) for weather data
- Built with [smolagents](https://github.com/huggingface/smolagents)
- LLM support via LiteLLM + Ollama

---

**Ready to start?**

```bash
# For interactive AI agent
python starter.py

# For template creation
python create_template.py
```

Happy templating! 🎨
