import requests
import json

url = "http://localhost:5001/api/distinguish/questions/2"

# 测试PUT请求（使用不同的content-type）
try:
    headers = {"Content-Type": "application/json"}
    data = {"stem": "test"}
    response = requests.put(url, data=json.dumps(data), headers=headers)
    print(f"PUT Status: {response.status_code}")
    print(f"PUT Response: {response.text[:500]}")
except Exception as e:
    print(f"PUT Error: {e}")

# 测试OPTIONS请求
try:
    response = requests.options(url)
    print(f"OPTIONS Status: {response.status_code}")
    print(f"OPTIONS Headers: {response.headers}")
except Exception as e:
    print(f"OPTIONS Error: {e}")