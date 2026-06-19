import sqlite3
conn = sqlite3.connect('instance/quiz_system.db')
cursor = conn.cursor()

# 检查所有题目的状态
cursor.execute('SELECT id, question_id, status, correct_at_learning_count, completed FROM practice_plan_records ORDER BY id')
rows = cursor.fetchall()

print('id | question_id | status | correct_at_learning_count | completed')
print('-' * 60)
for row in rows:
    print(f'{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}')

print()
print(f'总数: {len(rows)}')

# 检查有 correct_at_learning_count >= 2 的题目
cursor.execute('SELECT COUNT(*) FROM practice_plan_records WHERE correct_at_learning_count >= 2')
count = cursor.fetchone()[0]
print(f'correct_at_learning_count >= 2 的题目: {count}')

# 检查 completed=True 的题目
cursor.execute('SELECT COUNT(*) FROM practice_plan_records WHERE completed = 1')
count2 = cursor.fetchone()[0]
print(f'completed=True 的题目: {count2}')

# 检查 status='completed' 的题目
cursor.execute("SELECT COUNT(*) FROM practice_plan_records WHERE status = 'completed'")
count3 = cursor.fetchone()[0]
print(f'status="completed" 的题目: {count3}')

conn.close()