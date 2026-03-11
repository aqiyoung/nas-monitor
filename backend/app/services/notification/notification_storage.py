from typing import List, Dict, Optional
from app.models.notification.notification_models import NotificationChannel, NotificationPreference
import json
import os
from datetime import datetime
import uuid

class NotificationStorage:
    """通知存储服务"""
    
    def __init__(self, storage_dir: str = "./data"):
        """
        Args:
            storage_dir: 存储目录
        """
        self.storage_dir = storage_dir
        self.channels_file = os.path.join(storage_dir, "notification_channels.json")
        self.preferences_file = os.path.join(storage_dir, "notification_preferences.json")
        
        # 确保存储目录存在
        os.makedirs(storage_dir, exist_ok=True)
        
        # 初始化存储文件
        self._init_storage()
    
    def _init_storage(self):
        """初始化存储文件"""
        if not os.path.exists(self.channels_file):
            with open(self.channels_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        
        if not os.path.exists(self.preferences_file):
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _load_channels(self) -> List[Dict]:
        """加载通知渠道"""
        with open(self.channels_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_channels(self, channels: List[Dict]):
        """保存通知渠道"""
        with open(self.channels_file, 'w', encoding='utf-8') as f:
            json.dump(channels, f, ensure_ascii=False, indent=2)
    
    def _load_preferences(self) -> List[Dict]:
        """加载通知偏好设置"""
        with open(self.preferences_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_preferences(self, preferences: List[Dict]):
        """保存通知偏好设置"""
        with open(self.preferences_file, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, ensure_ascii=False, indent=2)
    
    def get_channels(self) -> List[NotificationChannel]:
        """获取所有通知渠道"""
        channels_data = self._load_channels()
        return [NotificationChannel(**channel) for channel in channels_data]
    
    def get_channel(self, channel_id: str) -> Optional[NotificationChannel]:
        """根据ID获取通知渠道"""
        channels_data = self._load_channels()
        for channel in channels_data:
            if channel['id'] == channel_id:
                return NotificationChannel(**channel)
        return None
    
    def create_channel(self, channel: NotificationChannel) -> NotificationChannel:
        """创建通知渠道"""
        channels_data = self._load_channels()
        
        # 生成唯一ID
        if not channel.id:
            channel.id = str(uuid.uuid4())
        
        # 保存渠道
        channels_data.append(channel.dict())
        self._save_channels(channels_data)
        
        return channel
    
    def update_channel(self, channel_id: str, updates: Dict) -> Optional[NotificationChannel]:
        """更新通知渠道"""
        channels_data = self._load_channels()
        updated = False
        
        for i, channel in enumerate(channels_data):
            if channel['id'] == channel_id:
                channels_data[i].update(updates)
                channels_data[i]['updated_at'] = datetime.now().isoformat()
                updated = True
                break
        
        if updated:
            self._save_channels(channels_data)
            return NotificationChannel(**channels_data[i])
        return None
    
    def delete_channel(self, channel_id: str) -> bool:
        """删除通知渠道"""
        channels_data = self._load_channels()
        new_channels = [c for c in channels_data if c['id'] != channel_id]
        
        if len(new_channels) != len(channels_data):
            self._save_channels(new_channels)
            return True
        return False
    
    def get_preferences(self) -> List[NotificationPreference]:
        """获取所有通知偏好设置"""
        preferences_data = self._load_preferences()
        return [NotificationPreference(**pref) for pref in preferences_data]
    
    def get_preference(self, user_id: str) -> Optional[NotificationPreference]:
        """根据用户ID获取通知偏好设置"""
        preferences_data = self._load_preferences()
        for pref in preferences_data:
            if pref['user_id'] == user_id:
                return NotificationPreference(**pref)
        return None
    
    def create_preference(self, preference: NotificationPreference) -> NotificationPreference:
        """创建通知偏好设置"""
        preferences_data = self._load_preferences()
        
        # 检查是否已存在该用户的偏好设置
        existing_index = None
        for i, pref in enumerate(preferences_data):
            if pref['user_id'] == preference.user_id:
                existing_index = i
                break
        
        if existing_index is not None:
            # 更新现有偏好设置
            preferences_data[existing_index] = preference.dict()
            preferences_data[existing_index]['updated_at'] = datetime.now().isoformat()
        else:
            # 创建新的偏好设置
            preferences_data.append(preference.dict())
        
        self._save_preferences(preferences_data)
        return preference
    
    def update_preference(self, user_id: str, updates: Dict) -> Optional[NotificationPreference]:
        """更新通知偏好设置"""
        preferences_data = self._load_preferences()
        updated = False
        
        for i, pref in enumerate(preferences_data):
            if pref['user_id'] == user_id:
                preferences_data[i].update(updates)
                preferences_data[i]['updated_at'] = datetime.now().isoformat()
                updated = True
                break
        
        if updated:
            self._save_preferences(preferences_data)
            return NotificationPreference(**preferences_data[i])
        return None

# 创建全局存储实例
storage = NotificationStorage()
