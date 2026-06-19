import sys
sys.stdout.reconfigure(encoding="utf-8")
fpath = r"D:\桌面\abc\frontend\src\App.vue"
with open(fpath, "r", encoding="utf-8") as f:
    c = f.read()
old = "{ active: 'distinguish' in $route.path }"
new = "{ active: $route.path.includes('distinguish') }"
if old in c:
    c = c.replace(old, new)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(c)
    print("Fixed!")
else:
    idx = c.find("distinguish")
    if idx > 0:
        print("Found distinguish at", idx)
        print("Context:", repr(c[idx-40:idx+60]))
    else:
        print("distinguish not found in file")
