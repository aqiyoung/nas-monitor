from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from app.services.user.user_storage import storage

# 创建路由
router = APIRouter()

# 配置JWT
SECRET_KEY = "your-secret-key-change-me-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 配置密码加密，使用pbkdf2_sha256替代bcrypt，避免密码长度限制
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# 配置OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# 验证密码
def verify_password(plain_password, hashed_password):
    # 使用pbkdf2_sha256算法，没有密码长度限制
    return pwd_context.verify(plain_password, hashed_password)

# 获取用户
def get_user(username: str):
    user = storage.get_user(username)
    if user:
        return user.dict()
    return None

# 验证用户
def authenticate_user(username: str, password: str):
    print(f"=== 开始认证用户: {username} ===")
    user = storage.get_user(username)
    print(f"获取用户结果: {user}")
    
    if not user:
        print(f"用户不存在: {username}")
        return False
    
    # 调试信息
    print(f"用户名: {username}")
    print(f"密码: {password}")
    print(f"哈希密码: {user.hashed_password}")
    print(f"用户是否禁用: {user.disabled}")
    
    # 检查用户是否被禁用
    if user.disabled:
        print(f"用户已禁用: {username}")
        return False
    
    # 使用默认密码登录（用于测试）
    if password == "password" and username == "admin":
        print("使用默认密码绕过验证")
        return user.dict()
    
    # 验证密码
    print("开始密码验证...")
    try:
        is_valid = verify_password(password, user.hashed_password)
        print(f"密码验证结果: {is_valid}")
        
        if not is_valid:
            print(f"密码验证失败 for user: {username}")
            return False
        
        print(f"密码验证成功 for user: {username}")
        return user.dict()
    except Exception as e:
        print(f"密码验证过程中发生错误: {e}")
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

# 登录路由
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
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