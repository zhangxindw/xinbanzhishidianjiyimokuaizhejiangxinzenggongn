import sys
sys.path.insert(0, r'd:\桌面\abc\backend')

from app import app, db, KnowledgePoint, KnowledgePointItem, to_html

with app.app_context():
    try:
        question = "测试问题"
        priority = "normal"
        mnemonic = "测试口诀"
        chapter_id = None
        items = [{"content": "第一条答案 {关键字}"}]
        
        print("创建 KnowledgePoint...")
        kp = KnowledgePoint(
            question=question,
            question_html=to_html(question),
            priority=priority,
            mnemonic=mnemonic,
            chapter_id=chapter_id
        )
        print(f"KnowledgePoint 创建成功: {kp}")
        
        db.session.add(kp)
        print("已添加到 session")
        
        db.session.flush()
        print(f"Flush 成功, ID: {kp.id}")
        
        for idx, item in enumerate(items):
            print(f"创建 item {idx}: {item}")
            kp_item = KnowledgePointItem(
                knowledge_point_id=kp.id,
                content=item.get('content', ''),
                content_html=to_html(item.get('content', '')),
                order=idx,
                blank_positions=item.get('blank_positions')
            )
            db.session.add(kp_item)
            print(f"Item {idx} 添加成功")
        
        db.session.commit()
        print("提交成功!")
        
        # 验证
        result = kp.to_dict()
        print(f"结果: {result}")
        
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"错误: {e}")
        traceback.print_exc()
