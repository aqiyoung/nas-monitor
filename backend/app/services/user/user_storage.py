import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from passlib.context import CryptContext
from app.models.user.user_models import User

# 配置密码加密
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class UserStorage:
    """用户存储服务"""
    
    def __init__(self, storage_dir: str = "./data"):
        self.storage_dir = storage_dir
        self.users: Dict[str, User] = {}
        
        # 确保存储目录存在
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # 加载数据
        self._load_data()
        
        # 如果没有管理员用户，创建一个默认管理员
        self._ensure_admin_user()
    
    def _load_data(self):
        """从文件加载数据"""
        users_file = os.path.join(self.storage_dir, "users.json")
        if os.path.exists(users_file):
            try:
                with open(users_file, "r") as f:
                    data = json.load(f)
                    for item in data:
                        # 转换日期字符串为datetime对象
                        # 处理不同格式的日期字符串，支持空格分隔和T分隔
                        for key in ["created_at", "updated_at"]:
                            if isinstance(item[key], str):
                                # 将空格分隔的日期格式转换为ISO格式（带T分隔符）
                                item[key] = item[key].replace(" ", "T")
                                item[key] = datetime.fromisoformat(item[key])
                        user = User(**item)
                        self.users[user.username] = user
            except Exception as e:
                print(f"Error loading users: {e}")
    
    def _save_data(self):
        """保存数据到文件"""
        users_file = os.path.join(self.storage_dir, "users.json")
        try:
            with open(users_file, "w") as f:
                data = [user.dict() for user in self.users.values()]
                json.dump(data, f, default=str, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def _ensure_admin_user(self):
        """确保存在管理员用户"""
        admin_user = None
        if "admin" not in self.users:
            # 创建新的管理员用户
            admin_user = User(
                id=str(uuid.uuid4()),
                username="admin",
                hashed_password=pwd_context.hash("password"),
                disabled=False,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.users[admin_user.username] = admin_user
            print(f"Created new admin user: {admin_user.username}")
        else:
            # 检查现有管理员用户的密码是否正确
            admin_user = self.users["admin"]
            if not pwd_context.verify("password", admin_user.hashed_password):
                # 更新密码为默认密码
                admin_user.hashed_password = pwd_context.hash("password")
                admin_user.updated_at = datetime.now()
                print(f"Updated admin password to default")
        
        if admin_user:
            self._save_data()
    
    def get_users(self) -> List[User]:
        """获取所有用户"""
        return list(self.users.values())
    
    def get_user(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.users.get(username)
    
    def create_user(self, username: str, password: str, disabled: bool = False) -> User:
        """创建用户"""
        if username in self.users:
            return None
        
        user = User(
            id=str(uuid.uuid4()),
            username=username,
            hashed_password=pwd_context.hash(password),
            disabled=disabled,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.users[username] = user
        self._save_data()
        return user
    
    def update_user(self, username: str, updates: dict) -> Optional[User]:
        """更新用户"""
        if username not in self.users:
            return None
        
        user = self.users[username]
        
        # 如果更新包含密码，哈希处理
        if "password" in updates:
            updates["hashed_password"] = pwd_context.hash(updates.pop("password"))
        
        # 更新用户属性
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        user.updated_at = datetime.now()
        self.users[username] = user
        self._save_data()
        return user
    
    def delete_user(self, username: str) -> bool:
        """删除用户"""
        # 不允许删除管理员用户
        if username == "admin":
            return False
        
        if username in self.users:
            del self.users[username]
            self._save_data()
            return True
        return False

# 创建全局存储实例
storage = UserStorage()