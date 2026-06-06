import urllib.request
import urllib.error

try:
    req = urllib.request.Request('http://127.0.0.1:5000/api/knowledge-points?page=1&per_page=5')
    response = urllib.request.urlopen(req)
    print(f"GET 状态码: {response.status}")
    print(f"GET 响应: {response.read().decode('utf-8')[:500]}")
except urllib.error.HTTPError as e:
    print(f"GET 错误: {e.code}")
    print(f"GET 响应: {e.read().decode('utf-8')[:500]}")
except Exception as e:
    print(f"GET 失败: {e}")
