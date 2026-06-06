import urllib.request
import urllib.error
import json

# 先测试 GET
print("=== 测试 GET ===")
try:
    req = urllib.request.Request('http://127.0.0.1:5000/api/knowledge-points?page=1&per_page=1')
    response = urllib.request.urlopen(req)
    print(f"GET 状态码: {response.status}")
except Exception as e:
    print(f"GET 失败: {e}")

# 测试 POST 不带 Content-Type
print("\n=== 测试 POST 不带 Content-Type ===")
try:
    req = urllib.request.Request(
        'http://127.0.0.1:5000/api/knowledge-points',
        data=b'{"question":"test"}',
        method='POST'
    )
    response = urllib.request.urlopen(req)
    print(f"POST 状态码: {response.status}")
except urllib.error.HTTPError as e:
    print(f"POST 错误: {e.code}")
    print(f"响应: {e.read().decode('utf-8')[:500]}")

# 测试 POST 带 Content-Type
print("\n=== 测试 POST 带 Content-Type ===")
try:
    req = urllib.request.Request(
        'http://127.0.0.1:5000/api/knowledge-points',
        data=b'{"question":"test"}',
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    response = urllib.request.urlopen(req)
    print(f"POST 状态码: {response.status}")
except urllib.error.HTTPError as e:
    print(f"POST 错误: {e.code}")
    print(f"响应: {e.read().decode('utf-8')[:500]}")
