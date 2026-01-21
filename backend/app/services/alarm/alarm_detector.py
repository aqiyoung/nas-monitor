import time
from datetime import datetime
from typing import Dict, List
from app.models.alarm.alarm_models import AlarmConfig, AlarmRecord
from app.services.system_service import get_cpu_usage, get_memory_usage, get_disk_usage
from app.services.docker_service import get_containers
from app.services.alarm.alarm_storage import storage

class AlarmDetector:
    """告警检测服务"""
    
    def __init__(self):
        self.metric_history: Dict[str, List[Dict]] = {
            "cpu_usage": [],
            "memory_usage": [],
            "disk_usage": []
        }
        self.max_history = 100  # 最大历史记录数
        
    def _update_metric_history(self, metric_type: str, value: float):
        """更新指标历史记录"""
        timestamp = time.time()
        self.metric_history[metric_type].append({"timestamp": timestamp, "value": value})
        
        # 保持历史记录数量在限制内
        if len(self.metric_history[metric_type]) > self.max_history:
            self.metric_history[metric_type] = self.metric_history[metric_type][-self.max_history:]
    
    def _check_threshold(self, metric_type: str, current_value: float, threshold: float, duration: int) -> bool:
        """检查指标是否在指定持续时间内超过阈值"""
        if current_value <= threshold:
            return False
        
        # 获取指定时间范围内的历史记录
        now = time.time()
        recent_metrics = [
            m for m in self.metric_history[metric_type] 
            if now - m["timestamp"] <= duration
        ]
        
        # 如果没有足够的历史记录，暂时不触发告警
        if len(recent_metrics) < 2:
            return False
        
        # 检查最近的指标是否都超过阈值
        return all(m["value"] > threshold for m in recent_metrics[-3:])  # 检查最近3个记录
    
    def detect_system_alerts(self):
        """检测系统告警"""
        # 获取系统指标
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        disk_usage = get_disk_usage()
        
        # 更新指标历史
        self._update_metric_history("cpu_usage", cpu_usage["total_usage"])
        self._update_metric_history("memory_usage", memory_usage["memory"]["percent"])
        
        # 获取系统告警配置
        system_configs = [
            config for config in storage.get_alarm_configs() 
            if config.alarm_type == "system" and config.enabled
        ]
        
        # 检查CPU高负载
        for config in [c for c in system_configs if c.sub_type == "cpu_high"]:
            if self._check_threshold(
                "cpu_usage", 
                cpu_usage["total_usage"], 
                config.threshold, 
                config.duration
            ):
                self._create_alarm_record(
                    alarm_type="system",
                    sub_type="cpu_high",
                    severity=config.severity,
                    message=f"CPU使用率过高: {cpu_usage['total_usage']:.1f}%",
                    details={"cpu_usage": cpu_usage}
                )
        
        # 检查内存不足
        for config in [c for c in system_configs if c.sub_type == "memory_low"]:
            if self._check_threshold(
                "memory_usage", 
                memory_usage["memory"]["percent"], 
                config.threshold, 
                config.duration
            ):
                self._create_alarm_record(
                    alarm_type="system",
                    sub_type="memory_low",
                    severity=config.severity,
                    message=f"内存使用率过高: {memory_usage['memory']['percent']:.1f}%",
                    details={"memory_usage": memory_usage}
                )
        
        # 检查磁盘空间不足
        for config in [c for c in system_configs if c.sub_type == "disk_low"]:
            for disk in disk_usage:
                if disk["percent"] > config.threshold:
                    self._create_alarm_record(
                        alarm_type="system",
                        sub_type="disk_low",
                        severity=config.severity,
                        message=f"磁盘空间不足: {disk['device']} {disk['percent']:.1f}%",
                        details={"disk": disk}
                    )
    
    def detect_docker_alerts(self):
        """检测Docker告警"""
        # 获取Docker容器
        containers = get_containers()
        
        # 获取Docker告警配置
        docker_configs = [
            config for config in storage.get_alarm_configs() 
            if config.alarm_type == "docker" and config.enabled
        ]
        
        # 检查容器异常退出
        for config in [c for c in docker_configs if c.sub_type == "container_exited"]:
            for container in containers:
                if container["status"] != "running":
                    self._create_alarm_record(
                        alarm_type="docker",
                        sub_type="container_exited",
                        severity=config.severity,
                        message=f"容器异常退出: {container['name']} ({container['status']})",
                        details={"container": container}
                    )
    
    def detect_network_alerts(self, client_ip: str = None):
        """检测网络告警"""
        if client_ip:
            # 获取网络告警配置
            network_configs = [
                config for config in storage.get_alarm_configs() 
                if config.alarm_type == "network" and config.enabled
            ]
            
            # 检查外部访问IP异常
            for config in [c for c in network_configs if c.sub_type == "external_ip"]:
                access_ip = storage.get_access_ip(client_ip)
                if access_ip and access_ip.is_blacklisted:
                    self._create_alarm_record(
                        alarm_type="network",
                        sub_type="external_ip",
                        severity=config.severity,
                        message=f"来自黑名单IP的访问: {client_ip}",
                        details={"ip_address": client_ip, "ip_info": access_ip.dict()}
                    )
    
    def _create_alarm_record(self, alarm_type: str, sub_type: str, severity: str, message: str, details: Dict):
        """创建告警记录"""
        # 检查是否已有相同类型的未处理告警
        existing_records = storage.get_alarm_records(limit=10)
        for record in existing_records:
            if (record.alarm_type == alarm_type and 
                record.sub_type == sub_type and 
                record.status == "unprocessed"):
                # 已有相同类型的未处理告警，不再创建新的
                return
        
        # 创建新的告警记录
        record = AlarmRecord(
            alarm_type=alarm_type,
            sub_type=sub_type,
            severity=severity,
            message=message,
            details=details
        )
        
        storage.create_alarm_record(record)
        print(f"Created alarm: {message}")
    
    def run_detection(self, client_ip: str = None):
        """运行所有告警检测"""
        self.detect_system_alerts()
        self.detect_docker_alerts()
        if client_ip:
            self.detect_network_alerts(client_ip)

# 创建全局告警检测器实例
alarm_detector = AlarmDetector()
