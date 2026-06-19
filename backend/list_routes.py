from app import app

# 打印所有注册的路由
print("=== Flask 注册的所有路由 ===")
for rule in app.url_map.iter_rules():
    methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
    print(f"{rule.endpoint}: {rule.rule} [{methods}]")