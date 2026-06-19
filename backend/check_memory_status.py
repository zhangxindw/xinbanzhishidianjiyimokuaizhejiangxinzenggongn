import sqlite3
from datetime import datetime

# 连接数据库
conn = sqlite3.connect('instance/quiz_system.db')
cursor = conn.cursor()

# 1. 检查当前所有刷题记录状态
print("=" * 80)
print("1. 当前所有刷题记录状态")
print("=" * 80)
cursor.execute('''
    SELECT id, question_id, status, correct_at_learning_count, completed, learning_repetition, next_review_date
    FROM practice_plan_records 
    ORDER BY id
''')
rows = cursor.fetchall()
print(f"{'ID':<5} {'Q_ID':<10} {'状态':<10} {'正确次数':<8} {'已完成':<6} {'重复次数':<8} {'下次复习'}")
print("-" * 80)
for row in rows:
    completed_str = '是' if row[4] else '否'
    print(f"{row[0]:<5} {row[1]:<10} {row[2]:<10} {row[3]:<8} {completed_str:<6} {row[5]:<8} {row[6]}")

# 2. 检查 correct_at_learning_count >= 2 但 completed = 0 的记录（这是 bug）
print("\n" + "=" * 80)
print("2. correct_at_learning_count >= 2 但 completed = 0 的记录（应该为0）")
print("=" * 80)
cursor.execute('''
    SELECT id, question_id, correct_at_learning_count, completed
    FROM practice_plan_records 
    WHERE correct_at_learning_count >= 2 AND completed = 0
''')
bug_rows = cursor.fetchall()
if bug_rows:
    print(f"发现 {len(bug_rows)} 条有问题的记录:")
    for row in bug_rows:
        print(f"  ID: {row[0]}, Q_ID: {row[1]}, correct_count: {row[2]}, completed: {row[3]}")
else:
    print("没有发现问题记录 ✓")

# 3. 检查 completed = 1 的记录
print("\n" + "=" * 80)
print("3. 已完成的记录")
print("=" * 80)
cursor.execute('''
    SELECT id, question_id, status, correct_at_learning_count, completed_at
    FROM practice_plan_records 
    WHERE completed = 1
''')
completed_rows = cursor.fetchall()
print(f"共 {len(completed_rows)} 条已完成记录")
for row in completed_rows:
    print(f"  ID: {row[0]}, Q_ID: {row[1]}, 状态: {row[2]}, 正确次数: {row[3]}, 完成时间: {row[4]}")

# 4. 统计信息
print("\n" + "=" * 80)
print("4. 统计信息")
print("=" * 80)
cursor.execute('SELECT COUNT(*) FROM practice_plan_records')
total = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM practice_plan_records WHERE status = "learning" AND completed = 0')
learning = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM practice_plan_records WHERE status = "reviewing" AND completed = 0')
reviewing = cursor.fetchone()[0]
cursor.execute('SELECT COUNT(*) FROM practice_plan_records WHERE completed = 1')
completed = cursor.fetchone()[0]

print(f"总记录数: {total}")
print(f"初学中（未完成）: {learning}")
print(f"复习中（未完成）: {reviewing}")
print(f"已完成: {completed}")

conn.close()
