import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'quiz_system.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("检查知识点表结构...")
cursor.execute("PRAGMA table_info(knowledge_points)")
for col in cursor.fetchall():
    print(f"  {col}")

print("\n检查所有知识点...")
cursor.execute("SELECT id, question, tag, answer, status, priority, chapter_id FROM knowledge_points")
for row in cursor.fetchall():
    print(f"  ID={row[0]}, question={row[1][:20]}, tag={row[2]}, answer={str(row[3])[:30]}, status={row[4]}, priority={row[5]}, chapter_id={row[6]}")

conn.close()
