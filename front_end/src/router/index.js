import { createRouter, createWebHistory } from 'vue-router'
import Todopage from '../views/Todopage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'todo',
      component: Todopage,
    },
  ],
})

export default router
