import sqlite3

# 连接到数据库
conn = sqlite3.connect('/root/backend/instance/quiz_system.db')
cursor = conn.cursor()

# 获取当前表结构
cursor.execute("PRAGMA table_info(memory_records)")
columns = cursor.fetchall()
column_names = [col[1] for col in columns]
print("Current columns:", column_names)

# 需要添加的列
columns_to_add = [
    ('result', 'TEXT', "''"),
    ('status', 'TEXT', "'learning'"),
    ('consecutive_correct', 'INTEGER', '0'),
    ('interval_days', 'INTEGER', '1'),
    ('learning_repetition', 'INTEGER', '0'),
    ('today_consecutive_count', 'INTEGER', '0'),
    ('created_at', 'TEXT', "datetime('now')"),
    ('updated_at', 'TEXT', "datetime('now')")
]

# 添加缺失的列
for col_name, col_type, default_val in columns_to_add:
    if col_name not in column_names:
        try:
            cursor.execute(f"ALTER TABLE memory_records ADD COLUMN {col_name} {col_type} DEFAULT {default_val}")
            print(f"Added column: {col_name}")
        except sqlite3.OperationalError as e:
            print(f"Error adding {col_name}: {e}")

conn.commit()
conn.close()

print("Migration completed!")