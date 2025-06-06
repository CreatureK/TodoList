# 实现对数据库的增删改查
# 使用sqlite sqlmodel

from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime
from typing import Optional

# 定义Todo模型
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)  # 主键
    title: str  # 标题
    content: str | None = None  # 内容
    completed: bool = Field(default=False)  # 是否完成
    create_time: datetime = Field(default_factory=datetime.now)  # 创建时间
    finish_time: Optional[datetime] = Field(default=None)  # 完成时间

# 定义数据库连接
sqlite_file_name = "TodoLists.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False} # 用于sqlite
engine = create_engine(sqlite_url, connect_args=connect_args) 

# 创建数据库表
def create_database():
    SQLModel.metadata.create_all(engine)

# 获取数据库会话
def get_session():
    with Session(engine) as session:
        yield session

# 增加数据
def add_todo(session: Session, title: str, content: str | None = None):
    # 创建时间会自动使用当前时间
    todo = Todo(title=title, content=content)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

# 查询全部数据
def get_todos(session: Session):
    statement = select(Todo) 
    todos = session.exec(statement).all() 
    return todos 


# 搜索str呈现所有title或内容符合的Todo
def search_todo(session: Session, str: str):
    statement = select(Todo).where(Todo.title.contains(str) | Todo.content.contains(str))
    todos = session.exec(statement).all()
    return todos

# 更新数据
def update_todo(session: Session, todo_id: int, title: str | None = None, 
                content: str | None = None, completed: bool | None = None):
    todo = session.exec(select(Todo).where(Todo.id == todo_id)).first()
    if todo:
        if title:
            todo.title = title
        if content:
            todo.content = content
        if completed is not None:
            # 如果状态从未完成变为已完成，记录完成时间
            if completed and not todo.completed:
                todo.finish_time = datetime.now()
            # 如果状态从已完成变为未完成，清除完成时间
            elif not completed and todo.completed:
                todo.finish_time = None
            todo.completed = completed
            
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
    return None

# 删除数据
def delete_todo(session: Session, todo_id: int):
    todo = session.exec(select(Todo).where(Todo.id == todo_id)).first()
    if todo:
        session.delete(todo)
        session.commit()
        return {"message": f"已删除ID为{todo_id}的待办事项"}
    return {"message": f"未找到ID为{todo_id}的待办事项"}

# 根据完成状态筛选Todo
def filter_todos_by_status(session: Session, completed: bool):
    statement = select(Todo).where(Todo.completed == completed)
    todos = session.exec(statement).all()
    return todos


