# 1. 使用官方 Python 轻量级镜像，减小体积
FROM python:3.9-slim

# 2. 设置容器内的工作目录
WORKDIR /app

# 3. 复制依赖清单并安装（利用 Docker 缓存层加速构建）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 复制项目所有文件到容器中
COPY . .

# 5. 声明端口（虽然 Render 会忽略这个，但写上符合规范）
EXPOSE 8000

# 6. 启动命令
# 注意：这里使用了 sh -c 来动态读取 Render/Cloud Run 提供的 PORT 环境变量
# 如果没有提供 PORT，默认使用 8000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
