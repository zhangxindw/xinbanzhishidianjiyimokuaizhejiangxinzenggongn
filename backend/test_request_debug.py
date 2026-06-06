import urllib.request
import urllib.error
import json

# 测试数据
test_data = {
    "question": "测试问题",
    "priority": "normal",
    "mnemonic": "测试口诀",
    "chapter_id": None,
    "items": [
        {"content": "第一条答案"}
    ]
}

print(f"发送的数据: {json.dumps(test_data, ensure_ascii=False)}")
print(f"数据长度: {len(json.dumps(test_data, ensure_ascii=False).encode('utf-8'))}")

req = urllib.request.Request(
    'http://127.0.0.1:5000/api/knowledge-points',
    data=json.dumps(test_data, ensure_ascii=False).encode('utf-8'),
    headers={'Content-Type': 'application/json; charset=utf-8'},
    method='POST'
)

print(f"\n请求头: {req.headers}")

try:
    response = urllib.request.urlopen(req)
    print(f"\n状态码: {response.status}")
    print(f"响应: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"\n错误状态码: {e.code}")
    body = e.read().decode('utf-8')
    print(f"错误响应体: {body}")
except Exception as e:
    print(f"\n请求失败: {e}")
    import traceback
    traceback.print_exc()
