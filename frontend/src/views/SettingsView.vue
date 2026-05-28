<template>
  <div class="settings-view">
    <div class="page-header">
      <h2>设置</h2>
      <p>个性化设置答题界面</p>
    </div>

    <div class="card">
      <h3>护眼模式</h3>
      <p style="color: #666; margin: 10px 0;">选择适合您的显示模式，减少眼睛疲劳</p>
      <el-radio-group v-model="eyeProtectionMode" @change="handleEyeProtectionChange">
        <el-radio label="none">关闭护眼模式</el-radio>
        <el-radio label="warm">暖黄护眼（经典纸质色调）</el-radio>
        <el-radio label="light">浅灰护眼（柔和白底）</el-radio>
        <el-radio label="dark">深色夜间模式（暗光环境）</el-radio>
      </el-radio-group>
    </div>

    <div class="card" style="margin-top: 20px;">
      <h3>字体大小</h3>
      <p style="color: #666; margin: 10px 0;">调整答题界面文字大小</p>
      <div class="font-size-preview">
        <el-slider v-model="fontSize" :min="12" :max="24" :step="1" show-stops @change="handleFontSizeChange" />
        <div class="preview-text" :style="{ fontSize: fontSize + 'px' }">
          预览文字：这是一段示例文本，用于预览字体大小效果
        </div>
      </div>
    </div>

    <div class="card" style="margin-top: 20px;">
      <h3>字体选择</h3>
      <p style="color: #666; margin: 10px 0;">选择您喜欢的字体风格</p>
      <el-select v-model="fontFamily" style="width: 200px;" @change="handleFontFamilyChange">
        <el-option label="微软雅黑" value="Microsoft YaHei" />
        <el-option label="宋体" value="SimSun" />
        <el-option label="黑体" value="SimHei" />
        <el-option label="仿宋" value="FangSong" />
      </el-select>
      <div class="preview-text" :style="{ fontFamily: fontFamily }" style="margin-top: 15px;">
        预览文字：这是一段示例文本，用于预览字体效果
      </div>
    </div>

    <div class="card" style="margin-top: 20px;">
      <h3>快捷键说明</h3>
      <el-table :data="shortcuts" style="width: 100%; margin-top: 15px;">
        <el-table-column prop="key" label="快捷键" width="120" />
        <el-table-column prop="action" label="功能" />
      </el-table>
    </div>

    <div style="margin-top: 20px; text-align: center;">
      <el-button type="primary" @click="resetSettings">恢复默认设置</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuizStore } from '@/store/quiz'
import { ElMessage } from 'element-plus'

const store = useQuizStore()

const eyeProtectionMode = ref('none')
const fontSize = ref(16)
const fontFamily = ref('Microsoft YaHei')

const shortcuts = [
  { key: '← / ↑', action: '上一题' },
  { key: '→ / ↓', action: '下一题' },
  { key: '1-6', action: '选择选项A-F' },
  { key: 'E', action: '开启/关闭护眼模式' }
]

const handleEyeProtectionChange = async () => {
  await store.updatePreferences({ eye_protection_mode: eyeProtectionMode.value })
  ElMessage.success('设置已保存')
}

const handleFontSizeChange = async () => {
  await store.updatePreferences({ font_size: fontSize.value })
  document.documentElement.style.setProperty('--font-size-base', `${fontSize.value}px`)
}

const handleFontFamilyChange = async () => {
  await store.updatePreferences({ font_family: fontFamily.value })
  document.documentElement.style.setProperty('--font-family-base', fontFamily.value)
}

const resetSettings = async () => {
  eyeProtectionMode.value = 'none'
  fontSize.value = 16
  fontFamily.value = 'Microsoft YaHei'
  await store.updatePreferences({
    eye_protection_mode: 'none',
    font_size: 16,
    font_family: 'Microsoft YaHei'
  })
  document.documentElement.style.setProperty('--font-size-base', '16px')
  document.documentElement.style.setProperty('--font-family-base', 'Microsoft YaHei')
  document.body.classList.remove('eye-protection-warm', 'eye-protection-light', 'eye-protection-dark')
  ElMessage.success('已恢复默认设置')
}

onMounted(async () => {
  await store.loadPreferences()
  eyeProtectionMode.value = store.preferences.eye_protection_mode || 'none'
  fontSize.value = store.preferences.font_size || 16
  fontFamily.value = store.preferences.font_family || 'Microsoft YaHei'
})
</script>

<style scoped>
.settings-view {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.font-size-preview {
  margin-top: 15px;
}

.preview-text {
  margin-top: 15px;
  padding: 15px;
  background: #f8f8ff;
  border-radius: 8px;
  line-height: 1.8;
}
</style>
