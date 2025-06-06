# 使用fastapi 和 uvicorn 运行 启动服务
# 使用router.py中的路由
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router
import uvicorn

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许的前端源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

app.include_router(router)

def main():
    # 使用uvicorn运行服务
    uvicorn.run(app, host="127.0.0.1", port=8080)

# 使用uvicorn运行服务
if __name__ == "__main__":
    main()

