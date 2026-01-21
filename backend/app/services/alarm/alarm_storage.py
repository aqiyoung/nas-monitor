import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from app.models.alarm.alarm_models import AlarmConfig, AlarmRecord, AccessIP

class AlarmStorage:
    """告警存储服务"""
    
    def __init__(self, storage_dir: str = "./data"):
        self.storage_dir = storage_dir
        self.alarm_configs: Dict[str, AlarmConfig] = {}
        self.alarm_records: Dict[str, AlarmRecord] = {}
        self.access_ips: Dict[str, AccessIP] = {}
        
        # 确保存储目录存在
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # 加载数据
        self._load_data()
    
    def _load_data(self):
        """从文件加载数据"""
        # 加载告警配置
        config_file = os.path.join(self.storage_dir, "alarm_configs.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    data = json.load(f)
                    for item in data:
                        # 转换日期字符串为datetime对象
                        item["created_at"] = datetime.fromisoformat(item["created_at"])
                        item["updated_at"] = datetime.fromisoformat(item["updated_at"])
                        config = AlarmConfig(**item)
                        self.alarm_configs[config.id] = config
            except Exception as e:
                print(f"Error loading alarm configs: {e}")
        
        # 加载告警记录
        records_file = os.path.join(self.storage_dir, "alarm_records.json")
        if os.path.exists(records_file):
            try:
                with open(records_file, "r") as f:
                    data = json.load(f)
                    for item in data:
                        # 转换日期字符串为datetime对象
                        item["timestamp"] = datetime.fromisoformat(item["timestamp"])
                        if item["processed_at"]:
                            item["processed_at"] = datetime.fromisoformat(item["processed_at"])
                        record = AlarmRecord(**item)
                        self.alarm_records[record.id] = record
            except Exception as e:
                print(f"Error loading alarm records: {e}")
        
        # 加载访问IP
        ips_file = os.path.join(self.storage_dir, "access_ips.json")
        if os.path.exists(ips_file):
            try:
                with open(ips_file, "r") as f:
                    data = json.load(f)
                    for item in data:
                        # 转换日期字符串为datetime对象
                        item["first_seen"] = datetime.fromisoformat(item["first_seen"])
                        item["last_seen"] = datetime.fromisoformat(item["last_seen"])
                        ip = AccessIP(**item)
                        self.access_ips[ip.ip_address] = ip
            except Exception as e:
                print(f"Error loading access ips: {e}")
    
    def _save_data(self):
        """保存数据到文件"""
        # 保存告警配置
        config_file = os.path.join(self.storage_dir, "alarm_configs.json")
        try:
            with open(config_file, "w") as f:
                data = [config.dict() for config in self.alarm_configs.values()]
                json.dump(data, f, default=str, indent=2)
        except Exception as e:
            print(f"Error saving alarm configs: {e}")
        
        # 保存告警记录（只保留最近1000条）
        records_file = os.path.join(self.storage_dir, "alarm_records.json")
        try:
            # 按时间排序，保留最近1000条
            sorted_records = sorted(
                self.alarm_records.values(), 
                key=lambda x: x.timestamp, 
                reverse=True
            )[:1000]
            data = [record.dict() for record in sorted_records]
            with open(records_file, "w") as f:
                json.dump(data, f, default=str, indent=2)
        except Exception as e:
            print(f"Error saving alarm records: {e}")
        
        # 保存访问IP
        ips_file = os.path.join(self.storage_dir, "access_ips.json")
        try:
            with open(ips_file, "w") as f:
                data = [ip.dict() for ip in self.access_ips.values()]
                json.dump(data, f, default=str, indent=2)
        except Exception as e:
            print(f"Error saving access ips: {e}")
    
    # 告警配置管理
    def get_alarm_configs(self) -> List[AlarmConfig]:
        """获取所有告警配置"""
        return list(self.alarm_configs.values())
    
    def get_alarm_config(self, config_id: str) -> Optional[AlarmConfig]:
        """根据ID获取告警配置"""
        return self.alarm_configs.get(config_id)
    
    def create_alarm_config(self, config: AlarmConfig) -> AlarmConfig:
        """创建告警配置"""
        self.alarm_configs[config.id] = config
        self._save_data()
        return config
    
    def update_alarm_config(self, config_id: str, updates: dict) -> Optional[AlarmConfig]:
        """更新告警配置"""
        if config_id not in self.alarm_configs:
            return None
        
        config = self.alarm_configs[config_id]
        for key, value in updates.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        config.updated_at = datetime.now()
        self.alarm_configs[config_id] = config
        self._save_data()
        return config
    
    def delete_alarm_config(self, config_id: str) -> bool:
        """删除告警配置"""
        if config_id in self.alarm_configs:
            del self.alarm_configs[config_id]
            self._save_data()
            return True
        return False
    
    # 告警记录管理
    def get_alarm_records(self, limit: int = 100, offset: int = 0) -> List[AlarmRecord]:
        """获取告警记录"""
        sorted_records = sorted(
            self.alarm_records.values(), 
            key=lambda x: x.timestamp, 
            reverse=True
        )
        return sorted_records[offset:offset+limit]
    
    def get_alarm_record(self, record_id: str) -> Optional[AlarmRecord]:
        """根据ID获取告警记录"""
        return self.alarm_records.get(record_id)
    
    def create_alarm_record(self, record: AlarmRecord) -> AlarmRecord:
        """创建告警记录"""
        self.alarm_records[record.id] = record
        self._save_data()
        return record
    
    def update_alarm_record(self, record_id: str, updates: dict) -> Optional[AlarmRecord]:
        """更新告警记录"""
        if record_id not in self.alarm_records:
            return None
        
        record = self.alarm_records[record_id]
        for key, value in updates.items():
            if hasattr(record, key):
                setattr(record, key, value)
        
        self.alarm_records[record_id] = record
        self._save_data()
        return record
    
    # 访问IP管理
    def get_access_ips(self) -> List[AccessIP]:
        """获取所有访问IP"""
        return list(self.access_ips.values())
    
    def get_access_ip(self, ip_address: str) -> Optional[AccessIP]:
        """根据IP地址获取访问记录"""
        return self.access_ips.get(ip_address)
    
    def create_or_update_access_ip(self, ip_address: str, country: str = "", region: str = "", city: str = "") -> AccessIP:
        """创建或更新访问IP记录"""
        if ip_address in self.access_ips:
            # 更新现有记录
            ip = self.access_ips[ip_address]
            ip.last_seen = datetime.now()
            ip.total_requests += 1
            if country:
                ip.country = country
            if region:
                ip.region = region
            if city:
                ip.city = city
        else:
            # 创建新记录
            ip = AccessIP(
                ip_address=ip_address,
                country=country,
                region=region,
                city=city
            )
        
        self.access_ips[ip_address] = ip
        self._save_data()
        return ip
    
    def update_access_ip_status(self, ip_address: str, is_blacklisted: bool) -> Optional[AccessIP]:
        """更新IP状态"""
        if ip_address in self.access_ips:
            ip = self.access_ips[ip_address]
            ip.is_blacklisted = is_blacklisted
            self.access_ips[ip_address] = ip
            self._save_data()
            return ip
        return None

# 创建全局存储实例
storage = AlarmStorage()
