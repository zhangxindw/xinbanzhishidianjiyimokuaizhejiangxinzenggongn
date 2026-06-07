import sqlite3

# 检查两个数据库
db_paths = [
    '/root/ruankaoshuati/backend/instance/quiz_system.db',
    '/root/backend/instance/quiz_system.db'
]

for db_path in db_paths:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(memory_records)')
        cols = cursor.fetchall()
        col_names = [c[1] for c in cols]
        print(f"\n{db_path}:")
        print(f"  Columns: {col_names}")
        print(f"  Has 'result': {'result' in col_names}")
        print(f"  Has 'status': {'status' in col_names}")
        conn.close()
    except Exception as e:
        print(f"\n{db_path}: Error - {e}")

# 找出正确的数据库并复制
print("\n--- Checking which DB has all required columns ---")
source_db = None
for db_path in db_paths:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(memory_records)')
        cols = cursor.fetchall()
        col_names = [c[1] for c in cols]
        if 'result' in col_names and 'status' in col_names:
            source_db = db_path
            print(f"Found complete DB: {db_path}")
        conn.close()
    except:
        pass

if source_db:
    import shutil
    target_db = '/root/backend/instance/quiz_system.db'
    print(f"Copying {source_db} to {target_db}...")
    shutil.copy2(source_db, target_db)
    print("Done!")
else:
    print("No complete DB found!")