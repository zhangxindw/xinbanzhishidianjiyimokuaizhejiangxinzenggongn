import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("PracticeView.vue","r",encoding="utf-8") as f:
    content = f.read()

changes = []

# 1. Add distinguish switch after shuffle options
old_switch = '                <div class="config-item" v-if="practiceMode === ' + "'sequential'" + '">\n                  <label>打乱选项:</label>\n                  <div class="switch-wrapper">\n                    <el-switch v-model="config.shuffleOptions" />\n                    <span class="switch-label">{{ config.shuffleOptions ? ' + "'已启用' : '已禁用'" + ' }}</span>\n                  </div>\n                </div>'
new_switch = old_switch + '\n                <div v-if="practiceMode === ' + "'memorize'" + ' ' + '|| practiceMode === ' + "'sequential'" + '" class="config-item">\n                  <label>辨析题模式:</label>\n                  <div class="switch-wrapper">\n                    <el-switch v-model="config.distinguishMode" />\n                    <span class="switch-label">{{ config.distinguishMode ? ' + "'已开启' : '已关闭'" + ' }}</span>\n                  </div>\n                </div>'

if old_switch in content:
    content = content.replace(old_switch, new_switch)
    changes.append("1. Added switch")
else:
    changes.append("1. Switch NOT found")

# 2-6: Add remaining changes...
print(changes[0])
with open("PracticeView.vue","w",encoding="utf-8") as f:
    f.write(content)
print("Done")
