import requests
import json

url = "http://localhost:5001/api/distinguish/questions/2"
data = {
    "stem": "test stem",
    "explanation": "test explanation",
    "options": [
        {"option_key": "A", "option_text": "test option A", "is_correct": True}
    ]
}

try:
    response = requests.put(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")