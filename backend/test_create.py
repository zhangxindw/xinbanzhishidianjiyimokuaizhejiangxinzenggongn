import urllib.request
import json

# 测试数据
test_data = {
    "question": "测试问题",
    "priority": "normal",
    "mnemonic": "测试口诀",
    "chapter_id": None,
    "items": [
        {"content": "第一条答案 {关键字}"},
        {"content": "第二条答案"}
    ]
}

req = urllib.request.Request(
    'http://127.0.0.1:5000/api/knowledge-points',
    data=json.dumps(test_data).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    response = urllib.request.urlopen(req)
    print(f"状态码: {response.status}")
    print(f"响应: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"错误状态码: {e.code}")
    print(f"错误响应: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"请求失败: {e}")
