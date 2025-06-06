# 实现路由
# 仅使用services.py中的方法

from fastapi import APIRouter, HTTPException
from services import add_todo_service, get_todos_service, update_todo_service, delete_todo_service, search_todo_service

router = APIRouter()

# 增加Todo
@router.post("/todos")
def add_todo(title: str, content: str | None = None):
    try:
        return add_todo_service(title, content)
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
def update_todo(todo_id: int, title: str | None = None, content: str | None = None, completed: bool | None = None):
    try:
        return update_todo_service(todo_id, title, content, completed)
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
def search_todo(str: str):
    try:
        return search_todo_service(str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

