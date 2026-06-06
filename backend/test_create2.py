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
    body = e.read().decode('utf-8')
    print(f"错误响应头: {dict(e.headers)}")
    print(f"错误响应体长度: {len(body)}")
    # 尝试解析 JSON
    try:
        data = json.loads(body)
        print(f"错误详情: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}")
    except:
        print(f"错误响应体: {body[:500]}")
except Exception as e:
    print(f"请求失败: {e}")
    import traceback
    traceback.print_exc()
