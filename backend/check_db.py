import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'quiz_system.db')
print(f"数据库路径: {db_path}")
print(f"数据库存在: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("\n所有表:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # 检查知识点表
    print("\n知识点表结构:")
    cursor.execute("PRAGMA table_info(knowledge_points)")
    for col in cursor.fetchall():
        print(f"  - {col}")
    
    # 检查知识点数据
    print("\n知识点数据:")
    cursor.execute("SELECT id, question, priority, chapter_id FROM knowledge_points")
    kps = cursor.fetchall()
    if kps:
        for kp in kps:
            print(f"  - ID: {kp[0]}, 问题: {kp[1][:30]}..., 优先级: {kp[2]}, 章节: {kp[3]}")
    else:
        print("  (无数据)")
    
    # 检查记忆记录
    print("\n记忆记录:")
    cursor.execute("SELECT id, knowledge_point_id, status FROM memory_records")
    records = cursor.fetchall()
    if records:
        for rec in records:
            print(f"  - ID: {rec[0]}, 知识点ID: {rec[1]}, 状态: {rec[2]}")
    else:
        print("  (无数据)")
    
    conn.close()
