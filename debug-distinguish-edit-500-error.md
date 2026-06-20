# Debug Session: distinguish-edit-500-error

## Problem Description
- **Symptom**: 编辑辨析题时后端返回500错误
- **Expected**: 编辑保存成功，返回更新后的数据
- **Reproduction**: 在辨析题管理页面点击编辑按钮，修改内容后点击保存

## Hypotheses
1. **H1**: 后端API路由未正确注册或与DELETE路由冲突（同路径不同方法）
2. **H2**: 数据库操作失败（外键约束、字段类型不匹配、事务问题）
3. **H3**: 前端发送的数据格式与后端期望不匹配（如缺少必需字段）
4. **H4**: 后端代码有运行时异常（如属性访问错误、类型错误）

## Status
[OPEN] - Instrumentation phase