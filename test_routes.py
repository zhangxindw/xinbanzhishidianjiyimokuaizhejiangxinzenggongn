import requests

# 检查Flask注册的路由
url = "http://localhost:5001/api/distinguish/questions/2"

# 测试GET请求
try:
    response = requests.get(url)
    print(f"GET Status: {response.status_code}")
    print(f"GET Response: {response.text[:200]}")
except Exception as e:
    print(f"GET Error: {e}")

# 测试DELETE请求
try:
    response = requests.delete(url)
    print(f"DELETE Status: {response.status_code}")
    print(f"DELETE Response: {response.text[:200]}")
except Exception as e:
    print(f"DELETE Error: {e}")

# 测试PUT请求
try:
    response = requests.put(url, json={"stem": "test"})
    print(f"PUT Status: {response.status_code}")
    print(f"PUT Response: {response.text[:200]}")
except Exception as e:
    print(f"PUT Error: {e}")