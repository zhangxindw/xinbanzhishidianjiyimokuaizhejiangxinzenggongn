import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("PracticeView.vue","r",encoding="utf-8") as f:
    content = f.read()

log = []

# 2: Add distinguish button in actions old_actions and new_actions
old_actions = (
    '<el-button v-if="!isInWrongBook(currentQuestion?.id)" type="warning" @click="addToWrongBook">'
    + '\u52a0\u5165\u9519\u9898\u672c</el-button>\n'
    + '            <el-button v-else type="success" @click="removeFromWrongBook">\u79fb\u51fa\u9519\u9898\u672c</el-button>\n'
    + '            <el-button type="primary" @click="nextQuestion" v-if="currentIndex < questions.length - 1">\u4e0b\u4e00\u9898</el-button>\n'
    + '            <el-button @click="finishPractice">\u5b8c\u6210\u7ec3\u4e60</el-button>'
)

new_actions = (
    '<el-button v-if="config.distinguishMode && currentQuestion?.id" type="primary" @click="openDistinguishDialog">'
    + '\u52a0\u5165\u8fa8\u6790\u9898</el-button>\n'
    + '            <el-button v-if="!isInWrongBook(currentQuestion?.id)" type="warning" @click="addToWrongBook">'
    + '\u52a0\u5165\u9519\u9898\u672c</el-button>\n'
    + '            <el-button v-else type="success" @click="removeFromWrongBook">\u79fb\u51fa\u9519\u9898\u672c</el-button>\n'
    + '            <el-button type="primary" @click="nextQuestion" v-if="currentIndex < questions.length - 1">\u4e0b\u4e00\u9898</el-button>\n'
    + '            <el-button @click="finishPractice">\u5b8c\u6210\u7ec3\u4e60</el-button>'
)

if old_actions in content:
    content = content.replace(old_actions, new_actions)
    log.append("2. Added action button")
else:
    log.append("2. Actions NOT found")

# 3: Add modal dialog
old_end = "  </div>\n</template>"
modal = (
    '  <!-- \u8fa8\u6790\u9898\u5f39\u7a97 -->\n'
    '  <el-dialog v-model="showDistinguishDialog" title="\u52a0\u5165\u8fa8\u6790\u9898" width="70%" :close-on-click-modal="false">\n'
    '    <div v-if="distinguishQuestionData" class="distinguish-dialog">\n'
    '      <div class="dialog-stem" v-html="distinguishQuestionData.stem_html || distinguishQuestionData.stem"></div>\n'
    '      <div v-for="(opt, idx) in distinguishOptions" :key="idx" class="dialog-option-row">\n'
    '        <div class="option-header">\n'
    '          <span class="option-key">{{ opt.key }}.</span>\n'
    '          <span class="option-text">{{ opt.text }}</span>\n'
    '          <el-tag :type="opt.is_correct ? \'success\' : \'danger\'" style="cursor:pointer" @click="toggleOptionCorrect(idx)">\n'
    '            {{ opt.is_correct ? \'\u6b63\u786e\' : \'\u9519\u8bef\' }}\n'
    '          </el-tag>\n'
    '        </div>\n'
    '        <div v-if="!opt.is_correct" class="corrected-input">\n'
    '          <el-input v-model="opt.corrected_text" placeholder="\u8bf7\u8f93\u5165\u6b63\u786e\u7684\u8868\u8ff0..." />\n'
    '        </div>\n'
    '      </div>\n'
    '      <div class="dialog-explanation" v-if="distinguishQuestionData.explanation">\n'
    '        <h4>\u89e3\u6790\uff1a</h4>\n'
    '        <div v-html="distinguishQuestionData.explanation"></div>\n'
    '      </div>\n'
    '    </div>\n'
    '    <template #footer>\n'
    '      <el-button @click="showDistinguishDialog = false">\u53d6\u6d88</el-button>\n'
    '      <el-button type="primary" @click="saveDistinguishQuestion">\u4fdd\u5b58</el-button>\n'
    '    </template>\n'
    '  </el-dialog>\n'
)

if old_end in content:
    content = content.replace(old_end, modal + old_end)
    log.append("3. Added modal")
else:
    log.append("3. Template end NOT found")

# 4: Add variables
old_var = "const practiceStarted = ref(false)"
new_var = old_var + "\nconst showDistinguishDialog = ref(false)\nconst distinguishQuestionData = ref(null)\nconst distinguishOptions = ref([])"

if old_var in content:
    content = content.replace(old_var, new_var)
    log.append("4. Added variables")
else:
    log.append("4. Variables NOT found")

# 5: Add config.distinguishMode
old_config = "const config = ref({\n    chapterIds: [],\n    shuffleOptions: false\n  })"
new_config = "const config = ref({\n    chapterIds: [],\n    shuffleOptions: false,\n    distinguishMode: false\n  })"
if old_config in content:
    content = content.replace(old_config, new_config)
    log.append("5. Added config")
else:
    idx = content.find("shuffleOptions: false")
    if idx > 0:
        end = content.index("\n", idx)
        old_part = content[idx:end]
        new_part = old_part + ",\n    distinguishMode: false"
        content = content.replace(old_part, new_part, 1)
        log.append("5. Added config (alt)")
    else:
        log.append("5. Config NOT found")

# 6: Add functions before </script>
script_end = "</script>"
funcs = (
    "\n\n// \u8fa8\u6790\u9898\u76f8\u5173\u51fd\u6570\n"
    "const openDistinguishDialog = () => {\n"
    "  const q = currentQuestion.value\n"
    "  if (!q) return\n"
    "  distinguishQuestionData.value = {\n"
    "    id: q.id,\n"
    "    stem: q.stem,\n"
    "    stem_html: q.stem_html,\n"
    "    explanation: q.explanation\n"
    "  }\n"
    "  const optionKeys = ['option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'option_f']\n"
    "  distinguishOptions.value = []\n"
    "  for (const key of optionKeys) {\n"
    "    if (q[key]) {\n"
    "      distinguishOptions.value.push({\n"
    "        key: key.replace('option_', '').toUpperCase(),\n"
    "        text: q[key],\n"
    "        is_correct: true,\n"
    "        corrected_text: ''\n"
    "      })\n"
    "    }\n"
    "  }\n"
    "  showDistinguishDialog.value = true\n"
    "}\n\n"
    "const toggleOptionCorrect = (idx) => {\n"
    "  distinguishOptions.value[idx].is_correct = !distinguishOptions.value[idx].is_correct\n"
    "}\n\n"
    "const saveDistinguishQuestion = async () => {\n"
    "  const q = distinguishQuestionData.value\n"
    "  if (!q) return\n"
    "  try {\n"
    "    const { default: axios } = await import('axios')\n"
    "    await axios.post('/api/distinguish/save', {\n"
    "      question_id: q.id,\n"
    "      options: distinguishOptions.value.map(o => ({\n"
    "        key: o.key,\n"
    "        text: o.text,\n"
    "        is_correct: o.is_correct,\n"
    "        corrected_text: o.is_correct ? null : (o.corrected_text || null)\n"
    "      }))\n"
    "    })\n"
    "    showDistinguishDialog.value = false\n"
    "    alert('\u5df2\u6dfb\u52a0\u5230\u8fa8\u6790\u9898\u7ba1\u7406')\n"
    "  } catch (e) {\n"
    "    console.error(e)\n"
    "    alert('\u4fdd\u5b58\u5931\u8d25')\n"
    "  }\n"
    "}\n"
)

content = content.replace(script_end, funcs + script_end)
log.append("6. Added functions")

with open("PracticeView.vue", "w", encoding="utf-8") as f:
    f.write(content)

for msg in log:
    print(msg)
print("Done")
