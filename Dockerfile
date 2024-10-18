# 使用 Alpine 作为基础镜像
FROM python:3.9-alpine

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口 8080
EXPOSE 8080

# 设置入口点为 app.py
CMD ["python", "app.py"]