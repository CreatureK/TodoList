<script setup>
import { RouterView } from 'vue-router'
import { ref, onMounted, watch } from 'vue'

// 主题状态
const isDarkMode = ref(false)

// 初始化主题
const initTheme = () => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    isDarkMode.value = savedTheme === 'dark'
    applyTheme(isDarkMode.value)
  } else {
    // 如果没有保存的主题，检查系统偏好
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    isDarkMode.value = prefersDark
    applyTheme(prefersDark)
  }
}

// 应用主题
const applyTheme = (dark) => {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
  if (dark) {
    document.body.classList.add('dark-mode')
  } else {
    document.body.classList.remove('dark-mode')
  }
}

// 监听localStorage的变化
const handleStorageChange = (event) => {
  if (event.key === 'theme') {
    const newTheme = event.newValue
    isDarkMode.value = newTheme === 'dark'
    applyTheme(isDarkMode.value)
  }
}

onMounted(() => {
  // 初始化主题
  initTheme()
  
  // 监听localStorage的变化
  window.addEventListener('storage', handleStorageChange)
  
  // 额外监听自定义事件 (用于同一个窗口内的通信)
  window.addEventListener('themeChange', (event) => {
    isDarkMode.value = event.detail.theme === 'dark'
    applyTheme(isDarkMode.value)
  })
})
</script>

<template>
  <div class="app-container" :class="{ 'dark-mode': isDarkMode }">
    <h1 class="app-title">TodoLists</h1>
    <RouterView />
  </div>
</template>

<style>
:root {
  --bg-color: #f5f5f5;
  --text-color: #333;
  --title-color: #2c3e50;
  --border-color: #e0e0e0;
  --transition: background-color 0.3s, color 0.3s;
}

[data-theme="dark"] {
  --bg-color: #1a1a1a;
  --text-color: #e0e0e0;
  --title-color: #f0f0f0;
  --border-color: #3a3a3a;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, "Microsoft YaHei", sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: var(--transition);
}

body.dark-mode {
  background-color: var(--bg-color);
  color: var(--text-color);
}

.app-container {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  padding: 1rem;
  transition: var(--transition);
}

.app-title {
  text-align: center;
  color: var(--title-color);
  margin-bottom: 1.5rem;
  font-size: 2rem;
  transition: var(--transition);
}

.dark-mode .app-title {
  color: var(--title-color);
}

@media (min-width: 768px) {
  .app-container {
    padding: 1.5rem;
  }
}

@media (min-width: 1200px) {
  .app-container {
    padding: 2rem;
  }
}
</style>
