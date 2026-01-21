from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel
import uuid

class AlarmConfig(BaseModel):
    """告警配置模型"""
    id: str = str(uuid.uuid4())
    alarm_type: str  # 告警类型：system, network, docker
    sub_type: str    # 子类型：cpu_high, memory_low, disk_low, etc.
    enabled: bool = True    # 是否启用
    threshold: float = 0.0  # 阈值
    duration: int = 30      # 持续时间（秒）
    severity: str = "warning"  # 告警级别：info, warning, critical
    push_methods: List[str] = []  # 推送方式
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class AlarmRecord(BaseModel):
    """告警记录模型"""
    id: str = str(uuid.uuid4())
    alarm_type: str
    sub_type: str
    severity: str
    message: str
    details: Dict = {}
    timestamp: datetime = datetime.now()
    status: str = "unprocessed"  # 状态：unprocessed, processed, ignored
    processed_at: Optional[datetime] = None
    processed_by: Optional[str] = None

class AccessIP(BaseModel):
    """访问IP模型"""
    id: str = str(uuid.uuid4())
    ip_address: str
    country: str = ""
    region: str = ""
    city: str = ""
    is_blacklisted: bool = False
    first_seen: datetime = datetime.now()
    last_seen: datetime = datetime.now()
    total_requests: int = 1

class AlarmStats(BaseModel):
    """告警统计模型"""
    total: int
    by_severity: Dict[str, int]
    by_type: Dict[str, int]
    recent: int  # 最近24小时的告警数

class AlarmCreateRequest(BaseModel):
    """创建告警配置请求模型"""
    alarm_type: str
    sub_type: str
    enabled: bool = True
    threshold: float = 0.0
    duration: int = 30
    severity: str = "warning"
    push_methods: List[str] = []

class AlarmUpdateRequest(BaseModel):
    """更新告警配置请求模型"""
    enabled: Optional[bool] = None
    threshold: Optional[float] = None
    duration: Optional[int] = None
    severity: Optional[str] = None
    push_methods: Optional[List[str]] = None

class AlarmStatusUpdateRequest(BaseModel):
    """更新告警状态请求模型"""
    status: str
    processed_by: Optional[str] = None

class IPStatusUpdateRequest(BaseModel):
    """更新IP状态请求模型"""
    is_blacklisted: bool