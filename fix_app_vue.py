import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("App.vue", "r", encoding="utf-8") as f:
    c = f.read()
old = "{ active: 'distinguish' in $route.path }"
new = "{ active: $route.path.includes('distinguish') }"
if old in c:
    c = c.replace(old, new)
    with open("App.vue", "w", encoding="utf-8") as f:
        f.write(c)
    print("Fixed!")
else:
    idx = c.find("distinguish")
    if idx > 0:
        print("Found at", idx, repr(c[idx-30:idx+50]))
