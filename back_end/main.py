# 使用fastapi 和 uvicorn 运行 启动服务
# 使用router.py中的路由
from fastapi import FastAPI
from router import router
import uvicorn

app = FastAPI()
app.include_router(router)

def main():
    # 使用uvicorn运行服务
    uvicorn.run(app, host="127.0.0.1", port=8080)

# 使用uvicorn运行服务
if __name__ == "__main__":
    main()

