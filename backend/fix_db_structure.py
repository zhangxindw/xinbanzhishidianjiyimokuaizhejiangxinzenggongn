import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'quiz_system.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("正在检查和修复数据库表结构...")

# 1. 检查 knowledge_points 表
print("\n检查 knowledge_points 表...")
cursor.execute("PRAGMA table_info(knowledge_points)")
columns = [col[1] for col in cursor.fetchall()]
print(f"现有列: {columns}")

# 检查是否需要添加或修改列
required_columns = ['question_html', 'priority', 'mnemonic', 'status', 'updated_at']
for col in required_columns:
    if col not in columns:
        try:
            if col == 'priority':
                cursor.execute(f"ALTER TABLE knowledge_points ADD COLUMN {col} TEXT DEFAULT 'normal'")
            elif col in ['question_html', 'mnemonic']:
                cursor.execute(f"ALTER TABLE knowledge_points ADD COLUMN {col} TEXT")
            elif col == 'status':
                cursor.execute(f"ALTER TABLE knowledge_points ADD COLUMN {col} TEXT DEFAULT 'active'")
            elif col == 'updated_at':
                cursor.execute(f"ALTER TABLE knowledge_points ADD COLUMN {col} DATETIME")
            print(f"  ✓ 添加列: {col}")
        except Exception as e:
            print(f"  ✕ 添加列 {col} 失败: {e}")
    else:
        print(f"  ✓ 列已存在: {col}")

# 2. 检查 knowledge_point_items 表
print("\n检查 knowledge_point_items 表...")
try:
    cursor.execute("PRAGMA table_info(knowledge_point_items)")
    kpi_columns = [col[1] for col in cursor.fetchall()]
    print(f"现有列: {kpi_columns}")
    
    required_kpi_columns = ['knowledge_point_id', 'content', 'content_html', 'order', 'blank_positions']
    for col in required_kpi_columns:
        if col not in kpi_columns:
            try:
                if col in ['content', 'content_html', 'blank_positions']:
                    cursor.execute(f"ALTER TABLE knowledge_point_items ADD COLUMN {col} TEXT")
                elif col == 'order':
                    cursor.execute(f"ALTER TABLE knowledge_point_items ADD COLUMN {col} INTEGER DEFAULT 0")
                print(f"  ✓ 添加列: {col}")
            except Exception as e:
                print(f"  ✕ 添加列 {col} 失败: {e}")
        else:
            print(f"  ✓ 列已存在: {col}")
except Exception as e:
    print(f"  检查表失败: {e}")

# 3. 检查 knowledge_point_relations 表
print("\n检查 knowledge_point_relations 表...")
try:
    cursor.execute("PRAGMA table_info(knowledge_point_relations)")
    kpr_columns = [col[1] for col in cursor.fetchall()]
    print(f"现有列: {kpr_columns}")
except Exception as e:
    print(f"  检查表失败: {e}")

# 4. 检查 memory_records 表
print("\n检查 memory_records 表...")
try:
    cursor.execute("PRAGMA table_info(memory_records)")
    mr_columns = [col[1] for col in cursor.fetchall()]
    print(f"现有列: {mr_columns}")
    
    required_mr_columns = ['consecutive_correct', 'interval_days', 'next_review_date', 
                          'last_review_date', 'review_count']
    for col in required_mr_columns:
        if col not in mr_columns:
            try:
                if col in ['consecutive_correct', 'interval_days', 'review_count']:
                    cursor.execute(f"ALTER TABLE memory_records ADD COLUMN {col} INTEGER DEFAULT 0")
                elif col in ['next_review_date', 'last_review_date']:
                    cursor.execute(f"ALTER TABLE memory_records ADD COLUMN {col} DATE")
                print(f"  ✓ 添加列: {col}")
            except Exception as e:
                print(f"  ✕ 添加列 {col} 失败: {e}")
        else:
            print(f"  ✓ 列已存在: {col}")
except Exception as e:
    print(f"  检查表失败: {e}")

conn.commit()
conn.close()
print("\n✓ 数据库结构检查完成!")
