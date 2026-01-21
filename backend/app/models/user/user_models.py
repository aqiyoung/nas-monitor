from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., description="用户名")
    disabled: bool = Field(default=False, description="是否禁用")

class UserCreate(UserBase):
    password: str = Field(..., description="密码")

class UserUpdate(UserBase):
    password: Optional[str] = Field(None, description="密码，可选")

class User(UserBase):
    id: str = Field(..., description="用户ID")
    hashed_password: str = Field(..., description="哈希密码")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")
    
    class Config:
        from_attributes = True