import sys
sys.path.insert(0, r'd:\桌面\abc\backend')

from app import app

with app.test_client() as client:
    # 测试 GET
    print("=== 测试 GET ===")
    resp = client.get('/api/knowledge-points?page=1&per_page=1')
    print(f"GET 状态码: {resp.status_code}")
    
    # 测试 POST
    print("\n=== 测试 POST ===")
    resp = client.post('/api/knowledge-points', 
                      json={"question": "测试", "priority": "normal", "items": []})
    print(f"POST 状态码: {resp.status_code}")
    print(f"POST 响应: {resp.get_json()}")
