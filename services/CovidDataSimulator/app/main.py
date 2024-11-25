# app/main.py
from fastapi import FastAPI
from api import endpoints
from config.settings import Server_IP, Server_PORT
import uvicorn

app = FastAPI()

# 包含所有的 API 路由
app.include_router(endpoints.router)

if __name__ == "__main__":
    uvicorn.run(app, host=Server_IP, port=Server_PORT)
