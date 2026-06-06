import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'quiz_system.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("检查知识点表...")
cursor.execute("SELECT COUNT(*) FROM knowledge_points")
count = cursor.fetchone()[0]
print(f"知识点总数: {count}")

if count > 0:
    cursor.execute("SELECT id, question, status FROM knowledge_points LIMIT 3")
    for row in cursor.fetchall():
        print(f"  ID={row[0]}, question={row[1][:30]}, status={row[2]}")

print("\n检查知识点条目表...")
cursor.execute("SELECT COUNT(*) FROM knowledge_point_items")
count = cursor.fetchone()[0]
print(f"知识点条目总数: {count}")

conn.close()
