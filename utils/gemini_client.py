import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_json(prompt: str) -> dict:
    """Send prompt to Gemini, expecting a JSON response. Returns parsed dict."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    raw = response.text.strip()
    # Strip markdown code fences if present
    if raw.startswith('```json'):
        raw = raw[7:]
    if raw.endswith('```'):
        raw = raw[:-3]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw_output": raw, "error": "Could not parse JSON"}
