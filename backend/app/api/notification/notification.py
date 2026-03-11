from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.notification.notification_models import (
    NotificationChannel, NotificationChannelCreate, NotificationChannelUpdate,
    NotificationPreference, NotificationPreferenceUpdate
)
from app.services.notification.notification_storage import storage
from app.api.auth import get_current_active_user

router = APIRouter()

# 通知渠道相关API
@router.get("/channels", response_model=List[NotificationChannel])
async def get_notification_channels(current_user: dict = Depends(get_current_active_user)):
    """获取所有通知渠道"""
    return storage.get_channels()

@router.get("/channels/{channel_id}", response_model=NotificationChannel)
async def get_notification_channel(channel_id: str, current_user: dict = Depends(get_current_active_user)):
    """根据ID获取通知渠道"""
    channel = storage.get_channel(channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="通知渠道不存在")
    return channel

@router.post("/channels", response_model=NotificationChannel)
async def create_notification_channel(channel_data: NotificationChannelCreate, current_user: dict = Depends(get_current_active_user)):
    """创建通知渠道"""
    channel = NotificationChannel(**channel_data.dict())
    return storage.create_channel(channel)

@router.put("/channels/{channel_id}", response_model=NotificationChannel)
async def update_notification_channel(channel_id: str, updates: NotificationChannelUpdate, current_user: dict = Depends(get_current_active_user)):
    """更新通知渠道"""
    update_dict = {k: v for k, v in updates.dict().items() if v is not None}
    channel = storage.update_channel(channel_id, update_dict)
    if not channel:
        raise HTTPException(status_code=404, detail="通知渠道不存在")
    return channel

@router.delete("/channels/{channel_id}")
async def delete_notification_channel(channel_id: str, current_user: dict = Depends(get_current_active_user)):
    """删除通知渠道"""
    if not storage.delete_channel(channel_id):
        raise HTTPException(status_code=404, detail="通知渠道不存在")
    return {"message": "通知渠道删除成功"}

# 通知偏好设置相关API
@router.get("/preferences", response_model=List[NotificationPreference])
async def get_notification_preferences(current_user: dict = Depends(get_current_active_user)):
    """获取所有通知偏好设置"""
    return storage.get_preferences()

@router.get("/preferences/{user_id}", response_model=NotificationPreference)
async def get_user_preference(user_id: str, current_user: dict = Depends(get_current_active_user)):
    """根据用户ID获取通知偏好设置"""
    preference = storage.get_preference(user_id)
    if not preference:
        raise HTTPException(status_code=404, detail="通知偏好设置不存在")
    return preference

@router.post("/preferences", response_model=NotificationPreference)
async def create_notification_preference(preference_data: NotificationPreference, current_user: dict = Depends(get_current_active_user)):
    """创建通知偏好设置"""
    return storage.create_preference(preference_data)

@router.put("/preferences/{user_id}", response_model=NotificationPreference)
async def update_notification_preference(user_id: str, updates: NotificationPreferenceUpdate, current_user: dict = Depends(get_current_active_user)):
    """更新通知偏好设置"""
    update_dict = {k: v for k, v in updates.dict().items() if v is not None}
    preference = storage.update_preference(user_id, update_dict)
    if not preference:
        raise HTTPException(status_code=404, detail="通知偏好设置不存在")
    return preference
