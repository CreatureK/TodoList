# 创建数据库

from repository import create_database, Todo, Session, engine, select
from datetime import datetime

# 创建数据库表结构
def init_database():
    print("正在创建数据库...")
    create_database()
    print("数据库表结构创建成功！")
    
    # 添加一些初始数据
    with Session(engine) as session:
        # 检查是否已存在数据
        statement = select(Todo)
        existing_todos = len(session.exec(statement).all())
        
        if existing_todos == 0:
            print("添加初始数据...")
            # 创建几条示例待办事项
            todo1 = Todo(
                title="学习FastAPI",
                content="完成FastAPI官方教程",
                completed=False,
                create_time=datetime.now()
            )
            
            # 已完成的任务，设置完成时间
            todo2 = Todo(
                title="学习Vue",
                content="学习Vue3基础知识",
                completed=True,
                create_time=datetime(2023, 5, 10, 10, 0, 0),
                finish_time=datetime(2023, 5, 12, 15, 30, 0)
            )
            
            todo3 = Todo(
                title="完成项目",
                content="完成待办事项系统开发",
                completed=False,
                create_time=datetime.now()
            )
            
            # 添加到session
            session.add(todo1)
            session.add(todo2)
            session.add(todo3)
            
            # 提交事务
            session.commit()
            print("初始数据添加成功！")
        else:
            print(f"数据库中已存在 {existing_todos} 条记录，跳过初始数据添加")
    
    print("数据库初始化完成！")

if __name__ == "__main__":
    init_database()


