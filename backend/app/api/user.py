from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.user.user_models import User, UserCreate, UserUpdate
from app.services.user.user_storage import storage
from app.api.auth import get_current_active_user

# 创建路由
router = APIRouter()

# 获取所有用户
@router.get("/", response_model=List[User])
async def get_users(current_user: dict = Depends(get_current_active_user)):
    """获取所有用户"""
    return storage.get_users()

# 获取单个用户
@router.get("/{username}", response_model=User)
async def get_user(username: str, current_user: dict = Depends(get_current_active_user)):
    """根据用户名获取用户"""
    user = storage.get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

# 创建用户
@router.post("/", response_model=User)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_active_user)):
    """创建新用户"""
    created_user = storage.create_user(user.username, user.password, user.disabled)
    if not created_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return created_user

# 更新用户
@router.put("/{username}", response_model=User)
async def update_user(username: str, user_update: UserUpdate, current_user: dict = Depends(get_current_active_user)):
    """更新用户信息"""
    # 转换为字典，只包含需要更新的字段
    update_data = user_update.dict(exclude_unset=True)
    
    # 更新用户
    updated_user = storage.update_user(username, update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return updated_user

# 删除用户
@router.delete("/{username}")
async def delete_user(username: str, current_user: dict = Depends(get_current_active_user)):
    """删除用户"""
    # 不允许删除当前登录用户
    if username == current_user["username"]:
        raise HTTPException(status_code=400, detail="不能删除当前登录用户")
    
    success = storage.delete_user(username)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在或无法删除")
    return {"message": "用户删除成功"}