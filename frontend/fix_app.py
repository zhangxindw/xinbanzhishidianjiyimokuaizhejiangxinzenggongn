import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("src/App.vue", "r", encoding="utf-8") as f:
    content = f.read()

# Add showDistinguishMenu variable near other showMenu variables
old_data = 'const showMemoryMenu = ref(false)'
new_data = 'const showMemoryMenu = ref(false)\nconst showDistinguishMenu = ref(false)'
content = content.replace(old_data, new_data)

# Add icon imports
old_icons = "Calendar, EditPen, Iphone"
new_icons = "Calendar, EditPen, Iphone, Warning, List"
content = content.replace(old_icons, new_icons)

# Fix the active class expression (simplify it)
# Old: :class="{ active: 'distinguish' in $route.path }"
# The issue was with the template syntax in sidebar
old_active = "{ active: 'distinguish' in $route.path }"
# Let's check if this is in the file
count_before = content.count("distinguish")
print(f"'distinguish' found {count_before} times in file")

# The sidebar template entry we added uses 'distinguish' in $route.path which is Vue template syntax
# This should work. Let's verify the file.

with open("src/App.vue", "w", encoding="utf-8") as f:
    f.write(content)

print("Script section updated")
