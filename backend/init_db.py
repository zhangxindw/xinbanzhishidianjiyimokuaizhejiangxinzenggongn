"""初始化数据库"""
from app import app, db
from models import Question, Chapter, QuestionType, KnowledgePoint, MemoryRecord

def init_database():
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("✓ 数据库表已创建")
        
        # 检查memory_records表结构
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('memory_records')]
        print(f"memory_records表的列: {columns}")
        
        # 检查是否有所需的字段
        required_fields = ['learning_repetition', 'today_consecutive_count']
        missing_fields = [f for f in required_fields if f not in columns]
        
        if missing_fields:
            print(f"\n缺少字段: {missing_fields}")
            print("请运行 update_db.py 来添加缺失的字段")
        else:
            print("\n✓ 所有必需字段已存在")

if __name__ == '__main__':
    init_database()
