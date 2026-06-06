import requests
import traceback

print("测试连接后端服务器...")
print(f"目标地址: http://localhost:5000/api/chapters")

try:
    response = requests.get('http://localhost:5000/api/chapters', timeout=5)
    print(f"HTTP状态码: {response.status_code}")
    print(f"响应内容长度: {len(response.text)}")
    print(f"响应内容: {response.text[:500]}")
except requests.exceptions.ConnectionError as e:
    print(f"连接错误: {e}")
    print("请检查后端服务器是否正常运行")
except requests.exceptions.Timeout as e:
    print(f"请求超时: {e}")
except Exception as e:
    print(f"其他错误: {e}")
    traceback.print_exc()