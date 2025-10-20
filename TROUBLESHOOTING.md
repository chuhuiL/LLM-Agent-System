# Troubleshooting Guide

## Common Template Errors

### Error: "Single '}' encountered in format string"

**Cause:** Template contains double curly braces `{{` or `}}` instead of single braces.

**Problem:**
```python
# ❌ WRONG - Double braces
template = "Weather for {{location}}: {{temperature}}°F"
```

**Solution:**
```python
# ✅ CORRECT - Single braces
template = "Weather for {location}: {temperature}°F"
```

**Why it happens:**
- In Python's `.format()` method, `{{` means "literal `{`" and `}}` means "literal `}`"
- So `{{location}}` becomes `{location}` (literal text, not a placeholder)
- Then the remaining `}` causes "Single '}' encountered" error

**How we fixed it:**
1. Added validation in `template_agent.py:80-108` to reject double braces
2. Improved error messages in `template_agent.py:140-145`
3. Fixed the bad template in `templates/templates.json`

---

### Error: "Missing data for placeholder 'xyz'"

**Cause:** Template has a placeholder that doesn't match the data keys.

**Example:**
```python
# Template expects {date} but weather data doesn't have a 'date' key
template = "Weather on {date}: {temperature}°F"

# Weather data only has:
weather_data = {
    "location": "Buffalo",
    "temperature": 71.1,
    "conditions": "Clear"
}
```

**Solution:** Only use placeholders that match your data:
- Weather data has: `location`, `country`, `temperature`, `feels_like`, `conditions`, `humidity`, `wind_speed`, `precipitation`
- Use only these in your weather templates

---

### Error: "Template 'xyz' not found"

**Cause:** Trying to use a template that doesn't exist.

**Solution:**
```
You: List all templates
```
This shows all available templates. Use the exact name.

---

### Error: "Mismatched braces"

**Cause:** Unequal number of `{` and `}` in template.

**Example:**
```python
# ❌ WRONG - Missing closing brace
template = "Weather: {temperature°F"

# ❌ WRONG - Extra closing brace
template = "Weather: {temperature}°F}"
```

**Solution:** Count your braces!
```python
# ✅ CORRECT
template = "Weather: {temperature}°F"
```

---

## LLM Agent Issues

### Issue: Agent doesn't provide code blocks

**Symptom:**
```
Error in code parsing:
Your code snippet is invalid, because the regex pattern <code>(.*?)</code> was not found
```

**Cause:** The LLM is explaining instead of executing code.

**Why:** The LLM encountered an error it can't fix and is giving up.

**Solution:**
1. Check the previous error messages
2. Fix the underlying issue (usually a template error)
3. Try again with a simpler query

---

### Issue: Agent reaches max steps without completing

**Symptom:** Agent stops at Step 10 with task incomplete

**Causes:**
1. Template errors causing retries
2. Query too complex
3. LLM confused about what to do

**Solutions:**
1. **Fix template errors first** - Run `list all templates` and `view template` to check
2. **Simplify query** - Break into smaller steps
3. **Be explicit** - "Get weather for Buffalo using weather_simple template"

---

## Template Best Practices

### ✅ DO:
- Use single braces: `{variable}`
- Use descriptive names: `{temperature}`, `{location}`
- Match data keys exactly
- Test templates before using them
- Add descriptions to templates

### ❌ DON'T:
- Use double braces: `{{variable}}`
- Use empty placeholders: `{}`
- Use spaces in placeholder names: `{my variable}`
- Use special characters: `{temp!}`, `{@location}`
- Mix different brace styles

---

## Quick Diagnostics

### Check Template Validity
```
You: View template content for daily_weather_forecast
```
Look for:
- Double braces `{{` or `}}`
- Mismatched braces
- Placeholders that don't match data

### Check Available Data
Weather data always has these keys:
```python
{
    "location": str,
    "country": str,
    "temperature": float,
    "feels_like": float,
    "conditions": str,
    "humidity": int,
    "wind_speed": float,
    "precipitation": float
}
```

### Test Template
```
You: Get weather for Buffalo

You: Generate from your_template with that data
```

---

## Getting Help

1. **Read error messages carefully** - They usually tell you exactly what's wrong
2. **Check TEMPLATE_AGENT_GUIDE.md** - Examples and patterns
3. **Check AGENT_LINKING_GUIDE.md** - Integration details
4. **List templates** - See what's available
5. **Start simple** - Use default templates first

---

## Fixed Issues

### ✅ Issue: Double Brace Template Error (Fixed)
- **Was:** Template used `{{variable}}` causing formatting errors
- **Fix:** Changed to `{variable}` in templates.json
- **Prevention:** Added validation to reject double braces

### ✅ Issue: Poor Error Messages (Fixed)
- **Was:** Generic "Error generating content" messages
- **Fix:** Added specific error handling for brace issues
- **Location:** template_agent.py:140-147

---

**Still having issues?** Check the error message against this guide!
