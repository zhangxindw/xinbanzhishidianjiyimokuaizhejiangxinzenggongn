<template>
  <div class="import-view">
    <div class="page-header">
      <h2>Excel题目导入</h2>
      <p>支持批量导入题目，可下载标准模板</p>
    </div>

    <div class="card">
      <div class="template-download">
        <h3>📥 下载导入模板</h3>
        <p style="color: #666; margin: 10px 0;">请先下载标准Excel模板，按格式填写题目信息</p>
        <el-button type="primary" @click="downloadTemplate">
          <el-icon><Download /></el-icon>
          下载Excel模板
        </el-button>
      </div>
    </div>

    <div class="card">
      <h3>📤 上传题目文件</h3>

      <div class="upload-area" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
        <input ref="fileInput" type="file" accept=".xls,.xlsx" style="display: none;" @change="handleFileSelect" />
        <el-icon style="font-size: 48px; color: #667eea; margin-bottom: 15px;"><UploadFilled /></el-icon>
        <p>点击或拖拽Excel文件到此处上传</p>
        <p style="color: #999; font-size: 12px; margin-top: 5px;">支持 .xls 和 .xlsx 格式</p>
      </div>

      <div v-if="uploading" style="margin-top: 20px;">
        <el-progress :percentage="uploadProgress" :status="uploadProgress === 100 ? 'success' : ''" />
        <p style="text-align: center; margin-top: 10px;">正在导入...</p>
      </div>

      <div v-if="importResult" class="import-result" :class="importResult.status">
        <h4>导入结果</h4>
        <div class="result-stats">
          <div class="stat-item success">
            <span class="stat-num">{{ importResult.data?.success_count || 0 }}</span>
            <span class="stat-label">成功</span>
          </div>
          <div class="stat-item warning">
            <span class="stat-num">{{ importResult.data?.duplicate_count || 0 }}</span>
            <span class="stat-label">跳过</span>
          </div>
          <div class="stat-item danger">
            <span class="stat-num">{{ importResult.data?.error_count || 0 }}</span>
            <span class="stat-label">失败</span>
          </div>
        </div>

        <div v-if="importResult.data?.error_rows?.length > 0" style="margin-top: 15px;">
          <h5>错误详情（前10条）</h5>
          <el-table :data="importResult.data.error_rows" style="margin-top: 10px;" size="small">
            <el-table-column prop="row" label="行号" width="80" />
            <el-table-column prop="error" label="错误原因" />
          </el-table>
        </div>
      </div>
    </div>

    <div class="card">
      <h3>📋 模板字段说明</h3>
      <el-table :data="fieldDescriptions" style="width: 100%; margin-top: 15px;">
        <el-table-column prop="field" label="字段名" width="120" />
        <el-table-column prop="required" label="必填" width="80">
          <template #default="{ row }">
            <el-tag :type="row.required ? 'danger' : 'success'" size="small">
              {{ row.required ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="说明" />
        <el-table-column prop="example" label="示例" width="150" />
      </el-table>
    </div>

    <div class="card">
      <h3>⚙️ 重复题目处理</h3>
      <el-checkbox-group v-model="duplicateOptions" style="margin-top: 15px;">
        <el-checkbox value="skip">跳过重复题目（推荐）</el-checkbox>
      </el-checkbox-group>
      <p style="color: #666; font-size: 12px; margin-top: 10px;">
        选择"跳过重复题目"将保留原题；不勾选则全部题目均按原样导入（即使重复也创建新题目）
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useQuizStore } from '@/store/quiz'
import { ElMessage } from 'element-plus'

const store = useQuizStore()

const fileInput = ref(null)
const uploading = ref(false)
const uploadProgress = ref(0)
const importResult = ref(null)
const duplicateOptions = ref(['skip'])

const fieldDescriptions = [
  { field: '题干', required: true, description: '题目文字内容，支持常规文字、简单符号', example: '以下哪个是Python的数据类型？' },
  { field: '选项A', required: true, description: '第一个备选答案内容', example: 'int' },
  { field: '选项B', required: true, description: '第二个备选答案内容', example: 'String' },
  { field: '选项C', required: true, description: '第三个备选答案内容', example: 'bool' },
  { field: '选项D', required: true, description: '第四个备选答案内容', example: 'list' },
  { field: '选项E', required: false, description: '第五个备选答案内容', example: 'array' },
  { field: '选项F', required: false, description: '第六个备选答案内容', example: 'tuple' },
  { field: '答案', required: true, description: '标准答案，单选填写单个字母（如A），多选填写多字母（如AC）', example: 'A' },
  { field: '解析', required: false, description: '题目答案讲解、知识点分析文字内容', example: 'int是Python的整数类型' },
  { field: '题型', required: true, description: '自定义题型名称', example: '单选题' }
]

const downloadTemplate = async () => {
  try {
    await store.downloadTemplate()
    ElMessage.success('模板下载成功')
  } catch (error) {
    ElMessage.error('模板下载失败')
  }
}

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    const ext = file.name.toLowerCase().split('.').pop()
    if (['xls', 'xlsx'].includes(ext)) {
      uploadFile(file)
    } else {
      ElMessage.error('请上传Excel文件(.xls或.xlsx格式)')
    }
  }
}

const handleDrop = (event) => {
  const file = event.dataTransfer.files[0]
  if (file) {
    const ext = file.name.toLowerCase().split('.').pop()
    if (['xls', 'xlsx'].includes(ext)) {
      uploadFile(file)
    } else {
      ElMessage.error('请上传Excel文件(.xls或.xlsx格式)')
    }
  }
}

const uploadFile = async (file) => {
  if (uploading.value) return

  uploading.value = true
  uploadProgress.value = 0
  importResult.value = null

  console.log('开始上传文件:', file.name)

  const progressTimer = setInterval(() => {
    if (uploadProgress.value < 90) {
      uploadProgress.value += Math.random() * 15
    }
  }, 200)

  try {
    // 根据选项决定处理方式
    const shouldSkip = duplicateOptions.value.includes('skip')
    const duplicateHandling = shouldSkip ? 'skip' : 'import_all'
    
    const result = await store.uploadQuestions(file, duplicateHandling)
    console.log('上传响应:', result)
    clearInterval(progressTimer)
    uploadProgress.value = 100
    importResult.value = result

    if (result.status === 'ok') {
      ElMessage.success(`导入完成！成功 ${result.data.success_count} 条`)
    } else {
      ElMessage.error(result.message || '导入失败')
    }
  } catch (error) {
    console.error('上传错误:', error)
    clearInterval(progressTimer)
    uploadProgress.value = 100
    
    // 尝试从错误响应中提取数据
    if (error.response && error.response.data) {
      importResult.value = error.response.data
      if (error.response.data.status === 'ok') {
        ElMessage.success(`导入完成！成功 ${error.response.data.data.success_count} 条`)
      } else {
        ElMessage.error(error.response.data.message || '导入失败')
      }
    } else {
      ElMessage.error('上传失败，请重试')
    }
  } finally {
    uploading.value = false
    fileInput.value.value = ''
  }
}
</script>

<style scoped>
.import-view {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.template-download {
  text-align: center;
  padding: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.template-download h3 {
  font-size: 20px;
  margin-bottom: 10px;
}

.upload-area {
  margin-top: 20px;
  padding: 60px 20px;
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-area:hover {
  border-color: #667eea;
  background: #f8f8ff;
}

.import-result {
  margin-top: 20px;
  padding: 20px;
  border-radius: 8px;
  background: #f8f8ff;
}

.import-result.success {
  background: #f6ffed;
  border: 1px solid #52c41a;
}

.import-result.error {
  background: #fff2f0;
  border: 1px solid #ff4d4f;
}

.result-stats {
  display: flex;
  gap: 30px;
  margin-top: 15px;
}

.stat-item {
  text-align: center;
}

.stat-num {
  display: block;
  font-size: 28px;
  font-weight: bold;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.stat-item.success .stat-num { color: #52c41a; }
.stat-item.warning .stat-num { color: #faad14; }
.stat-item.danger .stat-num { color: #ff4d4f; }
</style>
