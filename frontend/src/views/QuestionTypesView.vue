<template>
  <div class="question-types-view">
    <div class="page-header" style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <h2>题型管理</h2>
        <p>管理题目题型分类</p>
      </div>
      <el-button type="primary" @click="showDialog('create')">
        <el-icon><Plus /></el-icon>
        新建题型
      </el-button>
    </div>

    <div class="card">
      <el-table :data="questionTypes" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="题型名称" />
        <el-table-column prop="is_multiple" label="多选题" width="120">
          <template #default="{ row }">
            <el-tag :type="row.is_multiple ? 'warning' : 'success'" size="small">
              {{ row.is_multiple ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" type="text" @click="showDialog('edit', row)">编辑</el-button>
            <el-button size="small" type="text" danger @click="deleteType(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="400px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="题型名称">
          <el-input v-model="form.name" placeholder="如：单选题、多选题" />
        </el-form-item>
        <el-form-item label="多选题">
          <el-switch v-model="form.is_multiple" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveType">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useQuizStore } from '@/store/quiz'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useQuizStore()

const questionTypes = ref([])
const dialogVisible = ref(false)
const dialogType = ref('create')
const currentType = ref(null)
const form = reactive({
  name: '',
  is_multiple: false
})

const dialogTitle = computed(() => dialogType.value === 'create' ? '新建题型' : '编辑题型')

const loadQuestionTypes = async () => {
  await store.loadQuestionTypes()
  questionTypes.value = store.questionTypes
}

const showDialog = (type, data = null) => {
  dialogType.value = type
  currentType.value = data
  if (type === 'edit' && data) {
    form.name = data.name
    form.is_multiple = data.is_multiple
  } else {
    form.name = ''
    form.is_multiple = false
  }
  dialogVisible.value = true
}

const saveType = async () => {
  if (!form.name) {
    ElMessage.warning('请输入题型名称')
    return
  }

  try {
    if (dialogType.value === 'edit' && currentType.value) {
      await store.updateQuestionType(currentType.value.id, form)
      ElMessage.success('更新成功')
    } else {
      await store.createQuestionType(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadQuestionTypes()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const deleteType = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除题型"${row.name}"吗？`, '提示', { type: 'warning' })
    await store.deleteQuestionType(row.id)
    ElMessage.success('删除成功')
    loadQuestionTypes()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadQuestionTypes()
})
</script>

<style scoped>
.question-types-view {
  padding: 20px;
}
</style>
