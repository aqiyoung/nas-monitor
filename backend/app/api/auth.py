import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from app.services.user.user_storage import storage

logger = logging.getLogger("nas-monitor.auth")

# 登录请求模型
class LoginRequest(BaseModel):
    username: str
    password: str

# 创建路由
router = APIRouter()

# 配置JWT（从环境变量读取，生产环境必须修改！）
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production-use-openssl-rand-hex-32")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "30"))

# 配置密码加密
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 配置OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
    """获取用户"""
    user = storage.get_user(username)
    return user.dict() if user else None


def authenticate_user(username: str, password: str):
    """认证用户（严格验证，无后门）"""
    user = storage.get_user(username)

    if not user:
        logger.warning(f"Login attempt for non-existent user: {username}")
        return False

    if user.disabled:
        logger.warning(f"Login attempt for disabled user: {username}")
        return False

    try:
        is_valid = verify_password(password, user.hashed_password)
        if not is_valid:
            logger.warning(f"Invalid password for user: {username}")
            return False
        logger.info(f"User authenticated successfully: {username}")
        return user.dict()
    except Exception as e:
        logger.error(f"Authentication error for user {username}: {e}")
        return False

# 创建访问令牌
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 登录路由 - 同时支持form-data和json格式
@router.post("/login")
async def login(
    form_data: Optional[OAuth2PasswordRequestForm] = Depends(lambda: None),
    json_data: Optional[LoginRequest] = None
):
    # 处理json格式请求
    if json_data:
        user = authenticate_user(json_data.username, json_data.password)
    # 处理form-data格式请求
    elif form_data:
        user = authenticate_user(form_data.username, form_data.password)
    else:
        raise HTTPException(
            status_code=400,
            detail="请提供用户名和密码",
        )
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 验证令牌
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user

# 获取当前活跃用户
def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="用户已禁用")
    return current_user

# 测试路由，需要认证
@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    return current_user