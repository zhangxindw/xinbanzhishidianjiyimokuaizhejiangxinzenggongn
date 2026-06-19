import sqlite3
conn = sqlite3.connect('instance/quiz_system.db')
cursor = conn.cursor()
cursor.execute('SELECT id, question_id, status, correct_at_learning_count, learning_repetition, completed FROM practice_plan_records')
rows = cursor.fetchall()
print('id, question_id, status, correct_at_learning_count, learning_repetition, completed')
for row in rows:
    print(row)
conn.close()