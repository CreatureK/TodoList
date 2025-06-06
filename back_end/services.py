# 实现业务逻辑
# 仅使用repository.py中的方法

from repository import add_todo, get_todos, update_todo, delete_todo, search_todo, get_session as get_db_session, filter_todos_by_status
from sqlmodel import Session

# 获取session
def get_session():
    return next(get_db_session())

# 增加Todo
def add_todo_service(title: str, content: str | None = None):
    session = get_session()
    return add_todo(session, title, content)

# 获取所有Todo
def get_todos_service():
    session = get_session()
    return get_todos(session)

# 更新Todo
def update_todo_service(todo_id: int, title: str | None = None, content: str | None = None, completed: bool | None = None):
    session = get_session()
    return update_todo(session, todo_id, title, content, completed)

# 删除Todo
def delete_todo_service(todo_id: int):
    session = get_session()
    return delete_todo(session, todo_id)

# 搜索str呈现所有title或内容符合的Todo
def search_todo_service(str: str):
    session = get_session()
    return search_todo(session, str)

# 按完成状态筛选Todo
def filter_todos_by_status_service(completed: bool):
    session = get_session()
    return filter_todos_by_status(session, completed)







