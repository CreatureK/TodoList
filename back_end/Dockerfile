FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 使用国内镜像源安装依赖
RUN pip install --no-cache-dir --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
  pip install --no-cache-dir fastapi uvicorn sqlmodel -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 100

# 复制应用代码
COPY . /app/

# 创建数据库(如果不存在)
RUN python createdb.py

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
