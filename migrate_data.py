import sqlite3

conn = sqlite3.connect('/root/backend/instance/quiz_system.db')
cursor = conn.cursor()

# 将旧列的数据迁移到新列
cursor.execute("UPDATE memory_records SET next_review_date = next_review_at WHERE next_review_at IS NOT NULL AND next_review_at != ''")
print(f"Migrated {cursor.rowcount} rows for next_review_date")

cursor.execute("UPDATE memory_records SET last_review_date = last_reviewed_at WHERE last_reviewed_at IS NOT NULL AND last_reviewed_at != ''")
print(f"Migrated {cursor.rowcount} rows for last_review_date")

cursor.execute("UPDATE memory_records SET review_count = total_reviews WHERE total_reviews IS NOT NULL")
print(f"Migrated {cursor.rowcount} rows for review_count")

# 设置默认的next_review_date为今天
cursor.execute("UPDATE memory_records SET next_review_date = date('now') WHERE next_review_date IS NULL OR next_review_date = ''")
print(f"Set {cursor.rowcount} rows with default next_review_date")

conn.commit()
conn.close()
print("Data migration completed!")