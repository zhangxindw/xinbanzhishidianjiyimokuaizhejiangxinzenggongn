import requests
import json

# 测试反馈 API
url = 'http://localhost:5001/api/practice-plan/feedback?user_id=default_user'
headers = {'Content-Type': 'application/json'}

# 测试：答对 id=1 的题目（假设它的 correct_at_learning_count=1）
data = {
    'record_id': 1,
    'feedback': 'correct'
}

response = requests.post(url, headers=headers, json=data)
print('Status:', response.status_code)
print('Response:', json.dumps(response.json(), indent=2, ensure_ascii=False))

# 再次测试：答对 id=1 的题目（现在 correct_at_learning_count 应该是 2）
response2 = requests.post(url, headers=headers, json=data)
print('\n第二次答对:')
print('Status:', response2.status_code)
print('Response:', json.dumps(response2.json(), indent=2, ensure_ascii=False))