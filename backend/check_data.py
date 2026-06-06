import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'quiz_system.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("检查现有知识点数据...")

# 检查知识点
cursor.execute("SELECT id, question, answer FROM knowledge_points LIMIT 5")
kps = cursor.fetchall()

for kp in kps:
    print(f"\n知识点 ID: {kp[0]}")
    print(f"  问题: {kp[1]}")
    print(f"  答案: {kp[2]}")
    
    # 检查是否有对应的 items
    cursor.execute("SELECT id, content FROM knowledge_point_items WHERE knowledge_point_id = ?", (kp[0],))
    items = cursor.fetchall()
    print(f"  答案条目数: {len(items)}")
    if items:
        for item in items:
            print(f"    - 条目 {item[0]}: {item[1]}")

conn.close()
