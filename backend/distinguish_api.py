from flask import Blueprint, request, jsonify
from models import db, DistinguishQuestion, DistinguishOption, DistinguishRecord
from datetime import datetime, timedelta
import random

distinguish_bp = Blueprint("distinguish", __name__, url_prefix="/api/distinguish")

INTERVALS = [1, 2, 4, 7, 15, 30, 60, 120, 180, 365]

@distinguish_bp.route("/save", methods=["POST"])
def save_distinguish():
    user_id = request.args.get("user_id", "default_user")
    data = request.json
    question_id = data.get("question_id")
    options = data.get("options", [])
    if not question_id:
        return jsonify({"status": "error", "message": "question_id is required"}), 400
    dq = DistinguishQuestion(user_id=user_id, question_id=question_id)
    db.session.add(dq)
    db.session.flush()
    for opt in options:
        record = DistinguishOption(
            distinguish_question_id=dq.id,
            option_key=opt.get("key", ""),
            option_text=opt.get("text", ""),
            is_correct=opt.get("is_correct", True),
            corrected_text=opt.get("corrected_text", None)
        )
        db.session.add(record)
    db.session.commit()
    return jsonify({"status": "ok", "data": dq.to_dict()})

@distinguish_bp.route("/questions", methods=["GET"])
def list_distinguish():
    user_id = request.args.get("user_id", "default_user")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    pagination = DistinguishQuestion.query.filter_by(user_id=user_id).order_by(DistinguishQuestion.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({"status": "ok", "data": [q.to_dict() for q in pagination.items], "total": pagination.total, "pages": pagination.pages, "page": page})

@distinguish_bp.route("/questions/<int:qid>", methods=["DELETE"])
def delete_distinguish(qid):
    dq = DistinguishQuestion.query.get(qid)
    if not dq:
        return jsonify({"status": "error", "message": "not found"}), 404
    db.session.delete(dq)
    db.session.commit()
    return jsonify({"status": "ok", "message": "delete ok"})

@distinguish_bp.route("/questions/batch", methods=["DELETE"])
def batch_delete_distinguish():
    ids = request.json.get("ids", [])
    if not ids:
        return jsonify({"status": "error", "message": "ids required"}), 400
    DistinguishQuestion.query.filter(DistinguishQuestion.id.in_(ids)).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({"status": "ok", "message": f"deleted {len(ids)}"})

@distinguish_bp.route("/plan/add", methods=["POST"])
def add_to_plan():
    user_id = request.args.get("user_id", "default_user")
    option_ids = request.json.get("option_ids", [])
    if not option_ids:
        return jsonify({"status": "error", "message": "option_ids required"}), 400
    today = datetime.now().date()
    count = 0
    for opt_id in option_ids:
        if DistinguishRecord.query.filter_by(user_id=user_id, option_id=opt_id).first():
            continue
        opt = DistinguishOption.query.get(opt_id)
        if not opt:
            continue
        db.session.add(DistinguishRecord(
            user_id=user_id, option_id=opt_id, 
            status="learning", next_review_date=today,
            today_consecutive_count=0, learning_repetition=0
        ))
        count += 1
    db.session.commit()
    return jsonify({"status": "ok", "message": f"add {count} to plan"})

@distinguish_bp.route("/plan/statistics", methods=["GET"])
def plan_statistics():
    user_id = request.args.get("user_id", "default_user")
    today = datetime.now().date()
    total = DistinguishRecord.query.filter_by(user_id=user_id).count()
    learning = DistinguishRecord.query.filter_by(user_id=user_id, status="learning").count()
    reviewing = DistinguishRecord.query.filter_by(user_id=user_id, status="reviewing").count()
    overdue = DistinguishRecord.query.filter(
        DistinguishRecord.user_id == user_id, 
        DistinguishRecord.status == "reviewing", 
        DistinguishRecord.next_review_date <= today
    ).count()
    return jsonify({"status": "ok", "data": {
        "total_records": total, 
        "learning_count": learning, 
        "reviewing_count": reviewing, 
        "today_review_count": learning + overdue
    }})

def generate_practice_queue(user_id, current_record_id=None, feedback=None):
    """
    生成练习队列
    
    初始调用时：返回所有待学习+待复习题目（无预生成重复）
    带反馈调用时：在剩余队列中插入当前题目到指定位置
      - learning状态 + forgot：插入8题后
      - learning状态 + remembered：插入12题后
    """
    today = datetime.now().date()
    
    learning_records = list(DistinguishRecord.query.filter_by(user_id=user_id, status="learning").all())
    overdue_records = list(DistinguishRecord.query.filter(
        DistinguishRecord.user_id == user_id,
        DistinguishRecord.status == "reviewing",
        DistinguishRecord.next_review_date <= today
    ).all())
    
    # 复习题目随机打乱顺序
    random.shuffle(overdue_records)
    
    # 合并队列：先学习新题，后复习旧题
    queue = learning_records + overdue_records
    
    if not queue:
        return []
    
    # 如果有反馈（用户刚回答了一道题），需要将这道题插入到队列中
    if current_record_id and feedback:
        # 找到当前题目（可能在learning_records或overdue_records中，也可能刚转变状态）
        current_record = None
        for rec in learning_records + overdue_records:
            if rec.id == current_record_id:
                current_record = rec
                break
        
        # 如果在当前队列中找不到（状态刚改变），直接查询
        if not current_record:
            current_record = DistinguishRecord.query.get(current_record_id)
        
        if current_record:
            # 从队列中移除当前题目（稍后会重新插入）
            queue = [r for r in queue if r.id != current_record_id]
            
            # 如果队列为空，直接添加
            if not queue:
                queue.append(current_record)
            else:
                # 根据反馈决定间隔
                # learning状态：答错8题后再次出现，答对12题后验证
                # 注意：即使learning题目变成reviewing状态，也需要二次验证
                interval = 12 if feedback == "remembered" else 8
                
                # 计算插入位置
                insert_pos = interval
                
                if insert_pos >= len(queue):
                    # 插入到末尾
                    queue.append(current_record)
                else:
                    # 插入到指定位置之后
                    queue.insert(insert_pos, current_record)
    
    return queue

@distinguish_bp.route("/plan/tasks", methods=["GET"])
def plan_tasks():
    user_id = request.args.get("user_id", "default_user")
    tasks = generate_practice_queue(user_id)
    return jsonify({"status": "ok", "data": [t.to_dict() for t in tasks], "total": len(tasks)})

@distinguish_bp.route("/plan/feedback", methods=["POST"])
def plan_feedback():
    """辨析记忆反馈（艾宾浩斯遗忘曲线算法）"""
    user_id = request.args.get("user_id", "default_user")
    data = request.json
    record_id = data.get("record_id")
    fb = data.get("feedback")
    
    if not record_id or not fb:
        return jsonify({"status": "error", "message": "record_id and feedback required"}), 400
    
    record = DistinguishRecord.query.filter_by(id=record_id, user_id=user_id).first()
    if not record:
        return jsonify({"status": "error", "message": "not found"}), 404
    
    today = datetime.now().date()
    was_correct = fb == "remembered"
    
    # 记录原始状态和连续正确次数（在状态改变之前）
    original_status = record.status
    original_consecutive_count = record.today_consecutive_count
    
    # #region debug-point 1: 记录后端状态
    print(f"[DEBUG] record_id={record_id}, fb={fb}, original_status={original_status}, original_consecutive_count={original_consecutive_count}")
    # #endregion
    
    if record.status == "learning":
        if was_correct:
            record.today_consecutive_count += 1
            
            if record.today_consecutive_count >= 2:
                record.status = "reviewing"
                record.consecutive_correct = 1
                record.interval_days = INTERVALS[0]
                record.next_review_date = today + timedelta(days=1)
                record.today_consecutive_count = 0
        else:
            record.today_consecutive_count = 0
    else:
        if was_correct:
            if record.last_review_date != today:
                record.consecutive_correct += 1
            
            if record.consecutive_correct <= len(INTERVALS):
                record.interval_days = INTERVALS[record.consecutive_correct - 1]
            else:
                record.interval_days = min(int(record.interval_days * 1.5), 365)
            
            record.next_review_date = today + timedelta(days=record.interval_days)
        else:
            record.status = "learning"
            record.consecutive_correct = 0
            record.interval_days = 1
            record.next_review_date = today
            record.today_consecutive_count = 0
    
    record.last_review_date = today
    record.review_count += 1
    db.session.commit()
    
    # 计算是否需要重复该题目以及间隔
    # 关键：学习状态的题目，需要根据反馈决定是否重复
    # 第一次答对：12题后验证
    # 答错：8题后再次出现
    # 第二次答对：进入reviewing状态，当天不再重复
    repeat_info = None
    
    if original_status == "learning":
        if fb == "forgot":
            # 答错：8题后再次出现，直到答对
            repeat_info = {"interval": 8, "reason": "答错，8题后再次出现"}
        else:
            # 答对：只有第一次答对时需要验证（第二次答对进入复习状态）
            # original_consecutive_count是答对前的计数，所以等于0表示第一次答对
            if original_consecutive_count == 0:
                repeat_info = {"interval": 12, "reason": "答对，12题后验证"}
            # 如果original_consecutive_count >= 1，这是第二次答对，进入reviewing状态，当天不再重复
    
    # #region debug-point 2: 记录repeat_info返回值
    print(f"[DEBUG] repeat_info={repeat_info}")
    # #endregion
    
    result = {
        "status": "ok",
        "data": record.to_dict(),
        "repeat_info": repeat_info,
        "feedback_result": "remembered" if was_correct else "forgot"
    }
    
    return jsonify(result)

@distinguish_bp.route("/plan/practice", methods=["GET"])
def plan_practice():
    """获取当前应该练习的题目"""
    user_id = request.args.get("user_id", "default_user")
    tasks = generate_practice_queue(user_id)
    
    if tasks:
        return jsonify({"status": "ok", "data": tasks[0].to_dict(), "total": len(tasks)})
    else:
        return jsonify({"status": "ok", "data": None, "message": "暂无待复习的辨析题", "total": 0})

@distinguish_bp.route("/plan/record/<int:rid>", methods=["DELETE"])
def delete_plan_record(rid):
    record = DistinguishRecord.query.get(rid)
    if not record:
        return jsonify({"status": "error", "message": "not found"}), 404
    db.session.delete(record)
    db.session.commit()
    return jsonify({"status": "ok", "message": "removed"})

@distinguish_bp.route("/plan/clear-all", methods=["DELETE"])
def clear_all_plan():
    user_id = request.args.get("user_id", "default_user")
    DistinguishRecord.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({"status": "ok", "message": "cleared"})

def register_distinguish_api(app):
    app.register_blueprint(distinguish_bp)