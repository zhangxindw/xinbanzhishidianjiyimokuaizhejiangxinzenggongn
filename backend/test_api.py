import requests
import json

base_url = "http://127.0.0.1:5000"

print("测试创建知识点 API...")

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

try:
    response = requests.post(f"{base_url}/api/knowledge-points", json=test_data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"请求失败: {e}")
