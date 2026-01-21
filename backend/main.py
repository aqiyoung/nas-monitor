from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import system, network, io, docker

app = FastAPI(title="NAS Monitor API", version="1.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(system, prefix="/api/system", tags=["system"])
app.include_router(network, prefix="/api/network", tags=["network"])
app.include_router(io, prefix="/api/io", tags=["io"])
app.include_router(docker, prefix="/api/docker", tags=["docker"])

@app.get("/")
async def root():
    return {"message": "NAS Monitor API is running"}
