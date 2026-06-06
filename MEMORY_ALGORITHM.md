# 记忆算法说明文档

## 概述

本系统采用基于艾宾浩斯遗忘曲线的记忆算法，确保知识点在最佳时机得到复习。

## 一、知识点状态

系统维护两个核心状态：
- **初学中**：新添加的知识点，尚未熟练掌握
- **复习中**：已通过初学阶段，进入长期复习计划

## 二、用户反馈

用户在复习时提供三种反馈：
1. **背出了**：完全回忆正确，轻松无卡顿
2. **模糊**：部分回忆，有遗漏或不确定性
3. **背不出**：几乎没想起来或完全记错

## 三、初学中状态算法

### 3.1 状态转换规则

```
新知识点添加 → 初学中
      ↓
  用户反馈
      ↓
┌─────────────────────────────────────────┐
│ 背出了：today_consecutive_count + 1     │
│ 　　　　　安排在4个题目后再次出现         │
│ 　　　　　若连续2次背出了 → 进入复习中    │
├─────────────────────────────────────────┤
│ 模糊/背不出：today_consecutive_count = 0 │
│ 　　　　　安排在3个题目后再次出现         │
└─────────────────────────────────────────┘
```

### 3.2 具体逻辑

**用户点击"背出了"时：**
```python
today_consecutive_count += 1
if today_consecutive_count >= 2:
    # 连续2次背出了，毕业进入复习阶段
    status = 'reviewing'
    consecutive_correct = 1
    interval_days = 1  # 1天后复习
    next_review_date = today + 1天
else:
    # 继续初学循环
    learning_repetition = 4  # 4个题目后出现
```

**用户点击"模糊"或"背不出"时：**
```python
today_consecutive_count = 0  # 重置连续计数
learning_repetition = 3  # 3个题目后出现
```

### 3.3 循环机制

初学中知识点会在当天循环出现，直到满足条件：
- 连续2次"背出了" → 毕业
- 否则继续循环（最多循环次数不限）

## 四、复习中状态算法

### 4.1 间隔档位

复习间隔采用指数增长策略：

| 档位 | 间隔 | 说明 |
|------|------|------|
| 1 | 1天 | 初次复习 |
| 2 | 2天 | 连续2次背出 |
| 3 | 4天 | 连续3次背出 |
| 4 | 7天 | 连续4次背出 |
| 5 | 15天 | 连续5次背出 |
| 6 | 30天 | 连续6次背出 |
| 7 | 60天 | 连续7次背出 |
| 8 | 120天 | 连续8次背出 |
| ... | 180/365天 | 达到上限后缓慢增加 |

### 4.2 反馈处理

**用户点击"背出了"时：**
```python
consecutive_correct += 1
if consecutive_correct < len(intervals):
    interval_days = intervals[consecutive_correct]
else:
    # 已达最大档位，按1.5倍缓慢增加，最大365天
    interval_days = min(interval_days * 1.5, 365)
next_review_date = today + interval_days
```

**用户点击"模糊"时：**
```python
consecutive_correct = max(1, consecutive_correct - 1)
interval_days = intervals[consecutive_correct - 1]
next_review_date = today + interval_days
```

**用户点击"背不出"时：**
```python
status = 'learning'  # 打回初学中
consecutive_correct = 0
interval_days = 1
learning_repetition = 0  # 立即可复习
next_review_date = today
```

## 五、每日调度流程

### 5.1 任务生成规则

系统每天生成复习任务队列：

```
今日待复习队列 = 初学中所有任务 + 复习中逾期任务
      ↓
优先级排序：初学中优先 → 复习中逾期
```

### 5.2 队列优先级

1. **初学中任务**（最高优先级）
   - 必须在当天完成循环
   - 完成前阻塞新知识点学习

2. **复习中逾期任务**
   - 复习日期 ≤ 今天的任务
   - 未完成会累积到次日

### 5.3 学习新知识点的规则

- 必须先完成所有今日待复习任务
- 复习队列清空后才能学习新知识点
- 新知识点立即进入初学中状态

## 六、数据模型

### 6.1 MemoryRecord 字段

```python
class MemoryRecord:
    user_id: str                    # 用户ID
    knowledge_point_id: int         # 知识点ID
    status: str                     # 'learning' 或 'reviewing'
    
    # 初学中专用字段
    learning_repetition: int        # 还需要几个题目后出现（0=立即）
    today_consecutive_count: int    # 当天连续背出了几次
    
    # 复习中专用字段
    consecutive_correct: int        # 连续背出了几次
    interval_days: int              # 当前间隔天数
    
    # 通用字段
    next_review_date: date          # 下次复习日期
    last_review_date: date          # 上次复习日期
    review_count: int              # 总复习次数
```

## 七、API接口

### 7.1 获取今日任务
```
GET /api/memory/today-tasks?user_id=xxx
```

### 7.2 提交反馈
```
POST /api/memory/feedback?user_id=xxx
Body: {
    "kp_id": 1,
    "feedback": "remembered" | "fuzzy" | "forgot"
}
```

### 7.3 获取统计
```
GET /api/memory/statistics?user_id=xxx
Response: {
    "total_records": 100,
    "learning_count": 10,
    "reviewing_count": 90,
    "today_review_count": 5
}
```

## 八、示例场景

### 场景1：新知识点首次学习

1. 添加知识点 → 进入初学中，learning_repetition=0
2. 第一次复习，点击"背不出" → learning_repetition=3
3. 完成3个其他题目后，再次出现此知识点
4. 点击"模糊" → learning_repetition=3, today_consecutive_count=0
5. 完成3个其他题目后，再次出现
6. 点击"背出了" → learning_repetition=4, today_consecutive_count=1
7. 完成4个其他题目后，再次出现
8. 再次点击"背出了" → today_consecutive_count=2 → 毕业进入复习中，1天后复习

### 场景2：复习中遗忘

1. 知识点处于复习中，连续5次背出，间隔15天
2. 第6次复习时点击"模糊"
3. consecutive_correct=4，间隔变为7天

### 场景3：复习中完全遗忘

1. 知识点处于复习中，间隔30天
2. 复习时点击"背不出"
3. status='learning'，重新进入初学循环
4. learning_repetition=0，立即可再次复习

## 九、关键特性

✅ **高强度初学**：新知识点当天多次循环，直到熟练
✅ **防止假性记忆**：中途失败需重新开始，防止"虚假掌握"
✅ **指数增长间隔**：已掌握的知识点复习频率递减
✅ **智能降级**：模糊时适当缩短间隔，遗忘时重新学习
✅ **强制清债**：必须先完成复习任务，才能学习新知识
