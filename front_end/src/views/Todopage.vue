<script setup>
import { ref, reactive, onMounted, computed, watch, onUnmounted } from 'vue';
import { 
  ElMessage, 
  ElMessageBox 
} from 'element-plus';
import { Plus, Search, Moon, Sunny } from '@element-plus/icons-vue';
import todoApi from '../api/Todo';

// 主题状态
const isDarkMode = ref(false);

// 切换主题
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  document.documentElement.setAttribute('data-theme', isDarkMode.value ? 'dark' : 'light');
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light');
  
  // 触发自定义事件，通知其他组件（包括App.vue）
  window.dispatchEvent(new CustomEvent('themeChange', { 
    detail: { theme: isDarkMode.value ? 'dark' : 'light' } 
  }));
};

// 初始化主题
const initTheme = () => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    isDarkMode.value = savedTheme === 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
  } else {
    // 如果没有保存的主题，检查系统偏好
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    isDarkMode.value = prefersDark;
    document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
  }
};

// 响应式屏幕宽度
const screenWidth = ref(window.innerWidth);
const tableHeight = ref('450px');

// 监听窗口大小变化
const handleResize = () => {
  screenWidth.value = window.innerWidth;
  // 动态调整表格高度
  const windowHeight = window.innerHeight;
  tableHeight.value = `${windowHeight * 0.55}px`;
};

onMounted(() => {
  // 初始化主题
  initTheme();
  
  // 获取所有待办事项
  fetchAllTodos();
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize);
  handleResize(); // 初始调用一次
});

onUnmounted(() => {
  // 移除事件监听
  window.removeEventListener('resize', handleResize);
});

// 格式化日期时间
const formatDateTime = (date) => {
  const d = date instanceof Date ? date : new Date(date);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}:${String(d.getSeconds()).padStart(2, '0')}`;
};

// 待办事项状态选项
const statusOptions = [
  { label: '未完成', value: 0 },
  { label: '已完成', value: 1 }
];

// 表格数据
const tableData = ref([]);
const loading = ref(false);

// 搜索表单
const searchForm = reactive({
  keyword: '',
  status: ''
});

// 活跃状态过滤按钮
const activeStatus = ref('');

// 监听关键词变化自动搜索
watch(() => searchForm.keyword, async (newVal) => {
  if (newVal) {
    try {
      loading.value = true;
      const data = await todoApi.searchTodos(newVal);
      tableData.value = formatTodoData(data);
    } catch (error) {
      ElMessage.error(error.message || '搜索失败');
      console.error('搜索待办事项失败:', error);
    } finally {
      loading.value = false;
    }
  } else if (activeStatus.value) {
    // 如果关键词清空但有状态过滤，则应用状态过滤
    filterStatus(activeStatus.value);
  } else {
    // 如果关键词清空且没有状态过滤，则获取所有数据
    fetchAllTodos();
  }
}, { immediate: false });

// 格式化待办数据
const formatTodoData = (data) => {
  return data.map(item => ({
    id: item.id,
    title: item.title,
    content: item.content || '',
    status: item.completed ? 1 : 0,
    createTime: formatDateTime(item.create_time),
    finishTime: item.finish_time ? formatDateTime(item.finish_time) : null
  }));
};

// 筛选状态
const filterStatus = async (status) => {
  try {
    loading.value = true;
    activeStatus.value = status;
    
    if (status === '') {
      await fetchAllTodos();
    } else {
      const completed = status === '1';
      const data = await todoApi.filterTodosByStatus(completed);
      tableData.value = formatTodoData(data);
    }
  } catch (error) {
    ElMessage.error(error.message || '筛选数据失败');
    console.error('筛选待办事项失败:', error);
  } finally {
    loading.value = false;
  }
};

// 获取所有待办事项
const fetchAllTodos = async () => {
  try {
    loading.value = true;
    const data = await todoApi.getAllTodos();
    tableData.value = formatTodoData(data);
  } catch (error) {
    ElMessage.error(error.message || '获取数据失败');
    console.error('获取待办事项失败:', error);
  } finally {
    loading.value = false;
  }
};

// 新增/编辑表单
const todoForm = reactive({
  id: '',
  title: '',
  content: '',
  status: 0
});

// 表单规则
const rules = {
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' },
    { min: 2, max: 30, message: '长度在 2 到 30 个字符之间', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入内容', trigger: 'blur' }
  ]
};

// 弹窗相关
const dialogVisible = ref(false);
const dialogTitle = ref('新增待办事项');
const formRef = ref(null);

// 筛选后的数据
const filteredTableData = computed(() => {
  return tableData.value;
});

// 打开新增对话框
const handleAdd = () => {
  dialogTitle.value = '新增待办事项';
  resetForm();
  dialogVisible.value = true;
};

// 打开编辑对话框
const handleEdit = (row) => {
  dialogTitle.value = '编辑待办事项';
  resetForm();
  Object.assign(todoForm, row);
  dialogVisible.value = true;
};

// 删除待办事项
const handleDelete = (id) => {
  ElMessageBox.confirm('确认删除该待办事项?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await todoApi.deleteTodo(id);
      // 更新本地数据
      tableData.value = tableData.value.filter(item => item.id !== id);
      ElMessage.success('删除成功');
    } catch (error) {
      ElMessage.error(error.message || '删除失败');
      console.error('删除待办事项失败:', error);
    }
  }).catch(() => {});
};

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return;
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (todoForm.id) {
          // 编辑
          await todoApi.updateTodo(todoForm.id, {
            title: todoForm.title,
            content: todoForm.content,
            completed: todoForm.status === 1
          });
          ElMessage.success('更新成功');
        } else {
          // 新增
          await todoApi.addTodo(todoForm.title, todoForm.content);
          ElMessage.success('添加成功');
        }
        dialogVisible.value = false;
        // 重新获取所有待办事项
        if (activeStatus.value) {
          filterStatus(activeStatus.value);
        } else {
          fetchAllTodos();
        }
      } catch (error) {
        ElMessage.error(error.message || (todoForm.id ? '更新失败' : '添加失败'));
        console.error(todoForm.id ? '更新待办事项失败:' : '添加待办事项失败:', error);
      }
    }
  });
};

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields();
  }
  todoForm.id = '';
  todoForm.title = '';
  todoForm.content = '';
  todoForm.status = 0;
};

// 更改状态
const changeStatus = async (row) => {
  const newStatus = row.status === 0 ? 1 : 0;
  try {
    await todoApi.updateTodo(row.id, {
      completed: newStatus === 1
    });
    
    // 更新本地数据
    const index = tableData.value.findIndex(item => item.id === row.id);
    if (index !== -1) {
      tableData.value[index].status = newStatus;
      // 如果标记为完成，则记录完成时间；如果取消完成，则清除完成时间
      if (newStatus === 1) {
        tableData.value[index].finishTime = formatDateTime(new Date());
      } else {
        tableData.value[index].finishTime = null;
      }
    }
    
    ElMessage.success(`已${newStatus === 1 ? '完成' : '取消完成'}该待办事项`);
    
    // 如果有状态过滤，则更新列表
    if (activeStatus.value) {
      filterStatus(activeStatus.value);
    }
  } catch (error) {
    ElMessage.error(error.message || '状态更新失败');
    console.error('更新待办事项状态失败:', error);
  }
};
</script>

<template>
  <div class="todo-container" :class="{ 'dark-mode': isDarkMode }">
    <!-- 搜索区域 -->
    <el-card class="search-card">
      <div class="card-header">
        <div class="header-title">搜索筛选</div>
        <div class="theme-switch">
          <el-tooltip :content="isDarkMode ? '切换到浅色模式' : '切换到深色模式'" placement="left">
            <el-button 
              type="primary" 
              circle 
              @click="toggleTheme" 
              :icon="isDarkMode ? Sunny : Moon"
              size="small"
              class="theme-toggle-btn"
            ></el-button>
          </el-tooltip>
        </div>
      </div>
      <div class="search-area">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="关键词">
            <el-input 
              v-model="searchForm.keyword" 
              placeholder="请输入标题或内容" 
              clearable 
              :prefix-icon="Search"
            />
          </el-form-item>
        </el-form>
        <div class="status-filter">
          <el-button
            :type="activeStatus === '' ? 'primary' : 'info'"
            @click="filterStatus('')"
          >全部</el-button>
          <el-button
            :type="activeStatus === '1' ? 'primary' : 'info'"
            @click="filterStatus('1')"
          >已完成</el-button>
          <el-button
            :type="activeStatus === '0' ? 'primary' : 'info'"
            @click="filterStatus('0')"
          >未完成</el-button>
        </div>
      </div>
    </el-card>

    <!-- 表格区域 -->
    <el-card class="table-card">
      <template #header>
        <div class="card-header three-cols">
          <div class="header-title">待办事项列表</div>
          <!-- 操作按钮 -->
          <div class="operation-container">
            <el-button type="primary" @click="handleAdd" :icon="Plus">新增待办</el-button>
          </div>
          <div class="header-count">共 {{ filteredTableData.length }} 条记录</div>
        </div>
      </template>
      <el-empty v-if="filteredTableData.length === 0 && !loading" description="暂无待办事项"></el-empty>
      <el-table
        v-else
        :data="filteredTableData"
        style="width: 100%"
        border
        stripe
        highlight-current-row
        v-loading="loading"
        :max-height="tableHeight"
        :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
      >
        <el-table-column prop="id" label="ID" width="60" align="center" />
        <el-table-column prop="title" label="标题" min-width="120" show-overflow-tooltip />
        <el-table-column prop="content" label="内容" min-width="150" show-overflow-tooltip />
        <el-table-column label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'warning' : 'success'" size="small">
              {{ row.status === 0 ? '未完成' : '已完成' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="160" align="center" show-overflow-tooltip :class-name="screenWidth < 1100 ? 'hide-sm' : ''" />
        <el-table-column label="完成时间" width="160" align="center" show-overflow-tooltip :class-name="screenWidth < 1100 ? 'hide-sm' : ''">
          <template #default="{ row }">
            <span v-if="row.finishTime">{{ row.finishTime }}</span>
            <el-tag v-else type="info" size="small">未完成</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="120" align="center">
          <template #default="{ row }">
            <div class="operation-buttons">
              <el-tooltip :content="row.status === 0 ? '标记为已完成' : '标记为未完成'" placement="top">
                <el-button size="small" :type="row.status === 0 ? 'success' : 'warning'" @click="changeStatus(row)">
                  {{ row.status === 0 ? '完成' : '撤销' }}
                </el-button>
              </el-tooltip>
              <el-tooltip content="编辑待办事项" placement="top">
                <el-button size="small" type="primary" @click="handleEdit(row)">
                  编辑
                </el-button>
              </el-tooltip>
              <el-tooltip content="删除待办事项" placement="top">
                <el-button size="small" type="danger" @click="handleDelete(row.id)">
                  删除
                </el-button>
              </el-tooltip>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="formRef"
        :model="todoForm"
        :rules="rules"
        label-width="80px"
        style="max-width: 460px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="todoForm.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="todoForm.content"
            type="textarea"
            rows="4"
            placeholder="请输入内容"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="todoForm.status" placeholder="请选择状态" style="width: 100%">
            <el-option
              v-for="item in statusOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitForm">确 定</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
/* 基础样式 - 浅色模式 */
.todo-container {
  width: 100%;
  min-height: 100vh;
  box-sizing: border-box;
  padding: 20px;
  background-color: #f5f7fa;
  color: #303133;
  transition: background-color 0.3s, color 0.3s;
}

.search-card {
  margin-bottom: 20px;
  width: 100%;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
}

.operation-container {
  display: flex;
  justify-content: center;
}

.table-card {
  margin-bottom: 20px;
  width: 100%;
}

.operation-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 4px;
}

.operation-buttons .el-button {
  margin-left: 0;
  margin-right: 0;
}

/* 深色模式样式 */
.todo-container.dark-mode {
  background-color: #1a1a1a;
  color: #e0e0e0;
}

.todo-container.dark-mode :deep(.el-card) {
  background-color: #2c2c2c;
  color: #e0e0e0;
  border-color: #3a3a3a;
}

.todo-container.dark-mode :deep(.el-card__header) {
  border-bottom-color: #3a3a3a;
}

.todo-container.dark-mode :deep(.el-table) {
  background-color: #2c2c2c;
  color: #e0e0e0;
}

.todo-container.dark-mode :deep(.el-table tr) {
  background-color: #2c2c2c;
}

.todo-container.dark-mode :deep(.el-table td),
.todo-container.dark-mode :deep(.el-table th.el-table__cell) {
  background-color: #2c2c2c;
  border-bottom-color: #3a3a3a;
}

.todo-container.dark-mode :deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background-color: #363636;
}

.todo-container.dark-mode :deep(.el-table--enable-row-hover .el-table__body tr:hover > td) {
  background-color: #404040;
}

.todo-container.dark-mode :deep(.el-input__inner) {
  background-color: #363636;
  color: #e0e0e0;
  border-color: #4a4a4a;
}

.todo-container.dark-mode :deep(.el-input__wrapper) {
  background-color: #363636;
}

.todo-container.dark-mode :deep(.el-button) {
  border-color: #4a4a4a;
}

.todo-container.dark-mode :deep(.header-title),
.todo-container.dark-mode .header-title {
  color: #e0e0e0;
}

.todo-container.dark-mode :deep(.header-count),
.todo-container.dark-mode .header-count {
  color: #b0b0b0;
}

.todo-container.dark-mode :deep(.el-table__header-wrapper th.el-table__cell) {
  background-color: #363636 !important;
  color: #e0e0e0 !important;
}

.todo-container.dark-mode :deep(.el-dialog__body),
.todo-container.dark-mode :deep(.el-dialog__header),
.todo-container.dark-mode :deep(.el-dialog__footer) {
  background-color: #2c2c2c;
  color: #e0e0e0;
}

.theme-switch {
  margin-left: auto;
}

.theme-toggle-btn {
  transition: transform 0.3s;
}

.theme-toggle-btn:hover {
  transform: rotate(30deg);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-header.three-cols {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 10px;
}

.card-header.three-cols .header-title {
  text-align: left;
}

.card-header.three-cols .operation-container {
  justify-content: center;
}

.card-header.three-cols .header-count {
  text-align: right;
}

.header-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.header-count {
  font-size: 14px;
  color: #909399;
}

.el-button-group {
  display: flex;
}

.table-card :deep(.el-card__body) {
  padding-top: 0;
}

:deep(.hide-sm) {
  @media screen and (max-width: 1100px) {
    display: none;
  }
}

.table-card :deep(.el-table) {
  width: 100%;
}

/* 响应式样式 */
@media (max-width: 768px) {
  .todo-container {
    padding: 10px;
  }

  .card-header.three-cols {
    grid-template-columns: 1fr;
    grid-template-rows: repeat(3, auto);
    justify-items: center;
    gap: 10px;
  }

  .card-header.three-cols .header-title,
  .card-header.three-cols .header-count {
    text-align: center;
  }

  .search-form {
    flex-direction: column;
  }
  
  .search-form .el-form-item {
    margin-right: 0;
  }

  .table-card :deep(.el-table) {
    width: 100%;
    overflow-x: auto;
  }

  .operation-buttons {
    flex-direction: column;
  }
  
  .search-area {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .status-filter {
    width: 100%;
    justify-content: space-between;
  }
}

@media (min-width: 768px) and (max-width: 1200px) {
  .todo-container {
    padding: 15px;
  }
  
  .operation-buttons {
    flex-direction: column;
  }
}

@media (min-width: 1200px) {
  .todo-container {
    padding: 20px;
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.search-area {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.status-filter {
  display: flex;
  gap: 10px;
}
</style>
