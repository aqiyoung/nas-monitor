from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api import system, network, io, docker, auth
from app.api.auth import get_current_active_user

app = FastAPI(title="NAS Monitor API", version="1.0.0")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册无需认证的路由
app.include_router(auth, prefix="/api/auth", tags=["auth"])

# 注册需要认证的路由
app.include_router(system, prefix="/api/system", tags=["system"], dependencies=[Depends(get_current_active_user)])
app.include_router(network, prefix="/api/network", tags=["network"], dependencies=[Depends(get_current_active_user)])
app.include_router(io, prefix="/api/io", tags=["io"], dependencies=[Depends(get_current_active_user)])
app.include_router(docker, prefix="/api/docker", tags=["docker"], dependencies=[Depends(get_current_active_user)])

@app.get("/")
async def root():
    return {"message": "NAS Monitor API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
