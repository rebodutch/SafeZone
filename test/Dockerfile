# 使用官方的 Python 3 映像作為基礎
FROM python:3.12

# 設置工作目錄
WORKDIR /app

# 複製當前目錄下的所有文件到容器內的工作目錄
COPY . /app

# 指定執行 Python 腳本時的命令
CMD ["python", "test.py"]
