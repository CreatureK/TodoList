# 实现路由
# 仅使用services.py中的方法

from fastapi import APIRouter, HTTPException, Query
from services import (
    add_todo_service, 
    get_todos_service, 
    update_todo_service, 
    delete_todo_service, 
    search_todo_service,
    filter_todos_by_status_service
)
from typing import Optional
from pydantic import BaseModel


'''
# 解决 fastapi UI 加载不出来的问题
from fastapi import applications
from fastapi.openapi.docs import get_swagger_ui_html

def patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,**kwargs,
        swagger_js_url="https://cdn.bootcnd.net/ajax/libs/swagger-ui/5.6.2/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.bootcnd.net/ajax/libs/swagger-ui/5.6.2/swagger-ui.min.css"
    )

applications.get_swagger_ui_html = patch
'''


router = APIRouter()

# 定义请求体模型
class TodoCreate(BaseModel):
    title: str
    content: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    completed: Optional[bool] = None

# 增加Todo
@router.post("/todos")
def add_todo(todo: TodoCreate):
    try:
        return add_todo_service(todo.title, todo.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取所有Todo
@router.get("/todos")
def get_todos():
    try:
        return get_todos_service()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 更新Todo
@router.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdate):
    try:
        return update_todo_service(todo_id, todo.title, todo.content, todo.completed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# 删除Todo
@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    try:
        return delete_todo_service(todo_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 搜索str呈现所有title或内容符合的Todo
@router.get("/todos/search")
def search_todo(keyword: str = Query(..., description="搜索关键词")):
    try:
        return search_todo_service(keyword)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 按完成状态筛选Todo
@router.get("/todos/filter")
def filter_todos(completed: bool = Query(..., description="完成状态：True表示已完成，False表示未完成")):
    try:
        return filter_todos_by_status_service(completed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

