from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class NotificationChannel(BaseModel):
    """通知渠道"""
    id: str = Field(..., description="渠道ID")
    name: str = Field(..., description="渠道名称")
    type: str = Field(..., description="渠道类型: telegram, feishu, feishu_openclaw")
    enabled: bool = Field(default=True, description="是否启用")
    config: Dict[str, str] = Field(..., description="渠道配置")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")

class NotificationChannelCreate(BaseModel):
    """创建通知渠道"""
    name: str = Field(..., description="渠道名称")
    type: str = Field(..., description="渠道类型: telegram, feishu, feishu_openclaw")
    enabled: bool = Field(default=True, description="是否启用")
    config: Dict[str, str] = Field(..., description="渠道配置")

class NotificationChannelUpdate(BaseModel):
    """更新通知渠道"""
    name: Optional[str] = Field(None, description="渠道名称")
    enabled: Optional[bool] = Field(None, description="是否启用")
    config: Optional[Dict[str, str]] = Field(None, description="渠道配置")

class NotificationPreference(BaseModel):
    """通知偏好设置"""
    user_id: str = Field(..., description="用户ID")
    channels: List[str] = Field(default_factory=list, description="启用的通知渠道ID列表")
    message_types: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="消息类型偏好，键为消息类型，值为对应的通知渠道ID列表"
    )
    severity_levels: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="严重程度偏好，键为严重程度，值为对应的通知渠道ID列表"
    )
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")

class NotificationPreferenceUpdate(BaseModel):
    """更新通知偏好设置"""
    channels: Optional[List[str]] = Field(None, description="启用的通知渠道ID列表")
    message_types: Optional[Dict[str, List[str]]] = Field(None, description="消息类型偏好")
    severity_levels: Optional[Dict[str, List[str]]] = Field(None, description="严重程度偏好")
