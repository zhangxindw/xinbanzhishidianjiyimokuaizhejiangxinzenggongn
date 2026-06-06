"""更新数据库，添加新字段"""
import sqlite3
import os

def update_database():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'quiz_system.db')
    
    # 如果instance目录下没有，尝试根目录
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quiz_system.db')
    
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        print("数据库将在首次请求时自动创建")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查memory_records表结构
    cursor.execute("PRAGMA table_info(memory_records)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"当前memory_records表的列: {columns}")
    
    # 添加新字段
    if 'learning_repetition' not in columns:
        print("添加 learning_repetition 字段...")
        cursor.execute("ALTER TABLE memory_records ADD COLUMN learning_repetition INTEGER DEFAULT 0")
        print("✓ learning_repetition 字段已添加")
    
    if 'today_consecutive_count' not in columns:
        print("添加 today_consecutive_count 字段...")
        cursor.execute("ALTER TABLE memory_records ADD COLUMN today_consecutive_count INTEGER DEFAULT 0")
        print("✓ today_consecutive_count 字段已添加")
    
    conn.commit()
    
    # 验证更新
    cursor.execute("PRAGMA table_info(memory_records)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"\n更新后memory_records表的列: {columns}")
    
    conn.close()
    print("\n✓ 数据库更新完成！")

if __name__ == '__main__':
    update_database()
