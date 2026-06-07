import sqlite3

# 连接到数据库
conn = sqlite3.connect('/root/backend/instance/quiz_system.db')
cursor = conn.cursor()

# 添加缺失的列
try:
    cursor.execute("ALTER TABLE memory_records ADD COLUMN result TEXT DEFAULT ''")
    conn.commit()
    print("Column 'result' added successfully")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
finally:
    conn.close()