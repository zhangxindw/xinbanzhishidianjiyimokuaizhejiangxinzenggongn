import sys
sys.path.insert(0, r'd:\桌面\abc\backend')

import app
print(f"app 文件路径: {app.__file__}")

# 检查是否有 print 语句
import inspect
source = inspect.getsource(app.handle_knowledge_points)
if "收到 POST 请求" in source:
    print("✓ 找到了 print 语句")
else:
    print("✗ 没有找到 print 语句")
