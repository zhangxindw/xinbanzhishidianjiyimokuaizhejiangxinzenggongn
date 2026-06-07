import sqlite3

conn = sqlite3.connect('/root/backend/instance/quiz_system.db')
cursor = conn.cursor()

# 获取当前列
cursor.execute("PRAGMA table_info(memory_records)")
cols = cursor.fetchall()
col_names = [c[1] for c in cols]
print("Current columns:", col_names)

# 添加缺失的列
columns_to_add = [
    ('next_review_date', 'TEXT', "''"),
    ('last_review_date', 'TEXT', "''"),
    ('review_count', 'INTEGER', '0'),
]

for col_name, col_type, default_val in columns_to_add:
    if col_name not in col_names:
        try:
            cursor.execute(f"ALTER TABLE memory_records ADD COLUMN {col_name} {col_type} DEFAULT {default_val}")
            print(f"Added column: {col_name}")
        except sqlite3.OperationalError as e:
            print(f"Error adding {col_name}: {e}")

# 从旧列迁移数据到新列
if 'next_review_at' in col_names and 'next_review_date' in col_names:
    cursor.execute("UPDATE memory_records SET next_review_date = next_review_at WHERE next_review_date = ''")
    print("Migrated next_review_at to next_review_date")

if 'last_reviewed_at' in col_names and 'last_review_date' in col_names:
    cursor.execute("UPDATE memory_records SET last_review_date = last_reviewed_at WHERE last_review_date = ''")
    print("Migrated last_reviewed_at to last_review_date")

if 'total_reviews' in col_names and 'review_count' in col_names:
    cursor.execute("UPDATE memory_records SET review_count = total_reviews WHERE review_count = 0")
    print("Migrated total_reviews to review_count")

conn.commit()
conn.close()
print("Migration completed!")