import axios from 'axios';

// 创建axios实例
const request = axios.create({
  baseURL: 'http://localhost:8080', // 后端API的基础URL
  timeout: 10000,
});

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    let message = '请求出错';
    if (error.response) {
      // 服务器返回了错误状态码
      message = `错误状态码: ${error.response.status}, 信息: ${error.response.data.detail || '未知错误'}`;
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      message = '无法连接到服务器，请检查后端服务是否运行';
    } else {
      // 设置请求时发生错误
      message = error.message;
    }
    console.error(message, error);
    return Promise.reject({ message, error });
  }
);

// 获取所有待办事项
export const getAllTodos = () => {
  return request.get('/todos');
};

// 添加待办事项
export const addTodo = (title, content) => {
  return request.post('/todos', { title, content });
};

// 更新待办事项
export const updateTodo = (id, data) => {
  return request.put(`/todos/${id}`, data);
};

// 删除待办事项
export const deleteTodo = (id) => {
  return request.delete(`/todos/${id}`);
};

// 搜索待办事项
export const searchTodos = (keyword) => {
  return request.get(`/todos/search`, {
    params: { keyword }
  });
};

// 按完成状态筛选待办事项
export const filterTodosByStatus = (completed) => {
  return request.get(`/todos/filter`, {
    params: { completed }
  });
};

export default {
  getAllTodos,
  addTodo,
  updateTodo,
  deleteTodo,
  searchTodos,
  filterTodosByStatus
};
