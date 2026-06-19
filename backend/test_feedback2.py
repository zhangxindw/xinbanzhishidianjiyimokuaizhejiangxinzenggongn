import requests
import json

base_url = 'http://localhost:5001/api/practice-plan'

# 1. 检查当前任务列表
print('=== 1. 获取刷题任务 ===')
response = requests.get(f'{base_url}/tasks?user_id=default_user')
data = response.json()
print(f'API返回题目数量: {data.get("total")}')
print(f'后端 remaining: {data.get("remaining")}')
print()

# 2. 检查详情
print('=== 2. 今日待复习任务 ===')
response2 = requests.get(f'{base_url}/list?user_id=default_user')
data2 = response2.json()
print(f'今日待复习任务数量: {data2.get("total")}')
print()

# 3. 测试反馈API - 模拟答对 question_id=413 (id=2, 当前 correct_at_learning_count=0)
print('=== 3. 测试反馈API - 答对 id=2 (correct_at_learning_count=0) ===')
response3 = requests.post(
    f'{base_url}/feedback?user_id=default_user',
    headers={'Content-Type': 'application/json'},
    json={'record_id': 2, 'feedback': 'correct'}
)
print(f'状态码: {response3.status_code}')
result3 = response3.json()
print(f'返回数据: {json.dumps(result3, indent=2, ensure_ascii=False)}')
print()

# 4. 再次答对同一题 id=2 (现在 correct_at_learning_count 应该是 1)
print('=== 4. 再次答对 id=2 (correct_at_learning_count=1) ===')
response4 = requests.post(
    f'{base_url}/feedback?user_id=default_user',
    headers={'Content-Type': 'application/json'},
    json={'record_id': 2, 'feedback': 'correct'}
)
print(f'状态码: {response4.status_code}')
result4 = response4.json()
print(f'返回数据: {json.dumps(result4, indent=2, ensure_ascii=False)}')
print()

# 5. 检查数据库状态
print('=== 5. 检查数据库状态 ===')
import sqlite3
conn = sqlite3.connect('instance/quiz_system.db')
cursor = conn.cursor()
cursor.execute('SELECT id, question_id, status, correct_at_learning_count, completed FROM practice_plan_records WHERE id=2')
row = cursor.fetchone()
print(f'id=2 的记录: {row}')
conn.close()