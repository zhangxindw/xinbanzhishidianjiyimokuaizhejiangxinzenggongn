import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("PracticeView.vue","r",encoding="utf-8") as f:
    content = f.read()

old = """          <div v-if="practiceMode === 'memorize'" class="action-buttons">
            <el-button @click="toggleMastered" :type="isMastered ? 'success' : 'default'">
              {{ isMastered ? '已掌握' : '标记为已掌握' }}
            </el-button>
          </div>"""

new = """          <div v-if="practiceMode === 'memorize'" class="action-buttons">
            <el-button v-if="config.distinguishMode" type="primary" @click="openDistinguishDialog">加入辨析题</el-button>
            <el-button @click="toggleMastered" :type="isMastered ? 'success' : 'default'">
              {{ isMastered ? '已掌握' : '标记为已掌握' }}
            </el-button>
          </div>"""

if old in content:
    content = content.replace(old, new)
    with open("PracticeView.vue","w",encoding="utf-8") as f:
        f.write(content)
    print("Fixed! Added button to memorize mode")
else:
    idx = content.find("practiceMode === 'memorize'")
    print(f"Pattern not found at idx={idx}")
    if idx > 0:
        print(repr(content[idx-50:idx+200]))
