# 使用 Python 3.8 作为基础镜像
FROM python:3.8

# 设置工作目录为 /app
WORKDIR /app

# 将当前目录下的所有文件（除了.dockerignore中指定的文件）复制到 /app
COPY src/* /app
RUN mkdir /app/entity
COPY src/entity/* /app/entity
RUN mkdir /app/static
RUN mkdir /app/static/js
COPY src/static/js/* /app/static/js
RUN mkdir /app/templates
COPY src/templates/* /app/templates 
RUN mkdir /app/templates/admin
COPY src/templates/admin/* /app/templates/admin

# 安装依赖
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8080

# 执行应用
CMD ["python", "app.py"]
