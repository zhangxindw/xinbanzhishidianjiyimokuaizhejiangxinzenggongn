import requests
import json

# 获取刷题任务
url = 'http://localhost:5001/api/practice-plan/tasks?user_id=default_user'
response = requests.get(url)
data = response.json()
print('API 返回的题目数量:', data.get('total'))
print('后端 remaining:', data.get('remaining'))

# 获取今日待复习
url2 = 'http://localhost:5001/api/practice-plan/list?user_id=default_user'
response2 = requests.get(url2)
data2 = response2.json()
print('\n今日待复习任务数量:', data2.get('total'))

# 获取统计
url3 = 'http://localhost:5001/api/practice-plan/statistics?user_id=default_user'
response3 = requests.get(url3)
data3 = response3.json()
print('\n统计:', data3.get('data'))