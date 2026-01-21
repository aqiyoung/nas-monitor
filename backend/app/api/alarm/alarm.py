from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from app.models.alarm.alarm_models import (
    AlarmConfig, AlarmRecord, AccessIP, AlarmStats,
    AlarmCreateRequest, AlarmUpdateRequest, AlarmStatusUpdateRequest,
    IPStatusUpdateRequest
)
from app.services.alarm.alarm_storage import storage
from app.services.alarm.alarm_detector import alarm_detector
from app.api.auth import get_current_active_user
from datetime import datetime, timedelta

router = APIRouter()

# 告警配置相关API
@router.get("/configs", response_model=List[AlarmConfig])
async def get_alarm_configs(current_user: dict = Depends(get_current_active_user)):
    """获取所有告警配置"""
    return storage.get_alarm_configs()

@router.get("/configs/{config_id}", response_model=AlarmConfig)
async def get_alarm_config(config_id: str, current_user: dict = Depends(get_current_active_user)):
    """根据ID获取告警配置"""
    config = storage.get_alarm_config(config_id)
    if not config:
        raise HTTPException(status_code=404, detail="告警配置不存在")
    return config

@router.post("/configs", response_model=AlarmConfig)
async def create_alarm_config(config_data: AlarmCreateRequest, current_user: dict = Depends(get_current_active_user)):
    """创建告警配置"""
    config = AlarmConfig(**config_data.dict())
    return storage.create_alarm_config(config)

@router.put("/configs/{config_id}", response_model=AlarmConfig)
async def update_alarm_config(config_id: str, updates: AlarmUpdateRequest, current_user: dict = Depends(get_current_active_user)):
    """更新告警配置"""
    update_dict = {k: v for k, v in updates.dict().items() if v is not None}
    config = storage.update_alarm_config(config_id, update_dict)
    if not config:
        raise HTTPException(status_code=404, detail="告警配置不存在")
    return config

@router.delete("/configs/{config_id}")
async def delete_alarm_config(config_id: str, current_user: dict = Depends(get_current_active_user)):
    """删除告警配置"""
    if not storage.delete_alarm_config(config_id):
        raise HTTPException(status_code=404, detail="告警配置不存在")
    return {"message": "告警配置删除成功"}

# 告警记录相关API
@router.get("/records", response_model=List[AlarmRecord])
async def get_alarm_records(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: dict = Depends(get_current_active_user)
):
    """获取告警记录"""
    return storage.get_alarm_records(limit=limit, offset=offset)

@router.get("/records/{record_id}", response_model=AlarmRecord)
async def get_alarm_record(record_id: str, current_user: dict = Depends(get_current_active_user)):
    """根据ID获取告警记录"""
    record = storage.get_alarm_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="告警记录不存在")
    return record

@router.put("/records/{record_id}", response_model=AlarmRecord)
async def update_alarm_record(record_id: str, updates: AlarmStatusUpdateRequest, current_user: dict = Depends(get_current_active_user)):
    """更新告警记录状态"""
    update_dict = updates.dict()
    update_dict["processed_at"] = datetime.now()
    if updates.processed_by:
        update_dict["processed_by"] = updates.processed_by
    else:
        update_dict["processed_by"] = current_user.get("username", "system")
    
    record = storage.update_alarm_record(record_id, update_dict)
    if not record:
        raise HTTPException(status_code=404, detail="告警记录不存在")
    return record

# 访问IP相关API
@router.get("/access-ips", response_model=List[AccessIP])
async def get_access_ips(current_user: dict = Depends(get_current_active_user)):
    """获取所有访问IP"""
    return storage.get_access_ips()

@router.get("/access-ips/{ip_address}", response_model=AccessIP)
async def get_access_ip(ip_address: str, current_user: dict = Depends(get_current_active_user)):
    """根据IP地址获取访问记录"""
    ip = storage.get_access_ip(ip_address)
    if not ip:
        raise HTTPException(status_code=404, detail="IP访问记录不存在")
    return ip

@router.put("/access-ips/{ip_address}", response_model=AccessIP)
async def update_access_ip(ip_address: str, updates: IPStatusUpdateRequest, current_user: dict = Depends(get_current_active_user)):
    """更新IP状态"""
    ip = storage.update_access_ip_status(ip_address, updates.is_blacklisted)
    if not ip:
        raise HTTPException(status_code=404, detail="IP访问记录不存在")
    return ip

# 告警统计API
@router.get("/statistics", response_model=AlarmStats)
async def get_alarm_statistics(current_user: dict = Depends(get_current_active_user)):
    """获取告警统计信息"""
    records = storage.get_alarm_records(limit=1000)
    
    # 计算总告警数
    total = len(records)
    
    # 按严重程度统计
    by_severity = {"info": 0, "warning": 0, "critical": 0}
    for record in records:
        by_severity[record.severity] += 1
    
    # 按类型统计
    by_type = {}
    for record in records:
        type_key = f"{record.alarm_type}_{record.sub_type}"
        by_type[type_key] = by_type.get(type_key, 0) + 1
    
    # 计算最近24小时的告警数
    recent = len([r for r in records if r.timestamp >= datetime.now() - timedelta(days=1)])
    
    return AlarmStats(
        total=total,
        by_severity=by_severity,
        by_type=by_type,
        recent=recent
    )

# 手动触发告警检测
@router.post("/detect")
async def manual_detect_alerts(
    client_ip: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user)
):
    """手动触发告警检测"""
    alarm_detector.run_detection(client_ip)
    return {"message": "告警检测已触发"}

# 获取默认告警配置
def get_default_alarm_configs():
    """获取默认告警配置"""
    return [
        AlarmConfig(
            alarm_type="system",
            sub_type="cpu_high",
            enabled=True,
            threshold=80.0,
            duration=30,
            severity="warning",
            push_methods=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        AlarmConfig(
            alarm_type="system",
            sub_type="memory_low",
            enabled=True,
            threshold=85.0,
            duration=30,
            severity="warning",
            push_methods=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        AlarmConfig(
            alarm_type="system",
            sub_type="disk_low",
            enabled=True,
            threshold=90.0,
            duration=0,
            severity="critical",
            push_methods=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        AlarmConfig(
            alarm_type="docker",
            sub_type="container_exited",
            enabled=True,
            threshold=0.0,
            duration=0,
            severity="warning",
            push_methods=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        AlarmConfig(
            alarm_type="network",
            sub_type="external_ip",
            enabled=True,
            threshold=0.0,
            duration=0,
            severity="warning",
            push_methods=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]

# 初始化默认告警配置
def init_default_alarm_configs():
    """初始化默认告警配置"""
    configs = storage.get_alarm_configs()
    if not configs:
        for default_config in get_default_alarm_configs():
            storage.create_alarm_config(default_config)
        print("已初始化默认告警配置")

# 调用初始化函数
init_default_alarm_configs()
