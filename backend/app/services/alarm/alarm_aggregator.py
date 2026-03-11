from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from app.models.alarm.alarm_models import AlarmRecord

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AlarmAggregator:
    """告警聚合与抑制服务"""
    
    def __init__(self):
        # 存储最近的告警记录，用于聚合
        self.recent_alerts: Dict[str, List[AlarmRecord]] = {}
        # 聚合窗口时间（秒）
        self.aggregation_window = 60
        # 告警抑制时间（秒）
        self.suppression_window = 300
        # 告警计数阈值，超过此值则聚合
        self.aggregation_threshold = 3
    
    def should_suppress(self, alarm_type: str, sub_type: str, severity: str) -> bool:
        """检查是否应该抑制告警
        
        Args:
            alarm_type: 告警类型
            sub_type: 子类型
            severity: 严重程度
        
        Returns:
            bool: 是否应该抑制
        """
        key = f"{alarm_type}_{sub_type}"
        if key not in self.recent_alerts:
            return False
        
        # 获取最近的告警记录
        recent_records = self.recent_alerts[key]
        
        # 检查是否在抑制窗口内
        if recent_records:
            latest_record = recent_records[-1]
            time_diff = (datetime.now() - latest_record.timestamp).total_seconds()
            if time_diff < self.suppression_window:
                logger.info(f"告警 {key} 在抑制窗口内，跳过")
                return True
        
        return False
    
    def add_alarm(self, alarm: AlarmRecord) -> Optional[AlarmRecord]:
        """添加告警并进行聚合
        
        Args:
            alarm: 告警记录
        
        Returns:
            Optional[AlarmRecord]: 聚合后的告警记录，如果不需要聚合则返回None
        """
        key = f"{alarm.alarm_type}_{alarm.sub_type}"
        
        # 检查是否应该抑制
        if self.should_suppress(alarm.alarm_type, alarm.sub_type, alarm.severity):
            return None
        
        # 添加到最近告警列表
        if key not in self.recent_alerts:
            self.recent_alerts[key] = []
        
        # 清理过期的告警记录
        self._cleanup_old_alerts()
        
        # 添加新告警
        self.recent_alerts[key].append(alarm)
        
        # 检查是否需要聚合
        if len(self.recent_alerts[key]) >= self.aggregation_threshold:
            aggregated_alarm = self._aggregate_alerts(key)
            # 清空该类型的告警列表
            self.recent_alerts[key] = []
            return aggregated_alarm
        
        return None
    
    def _aggregate_alerts(self, key: str) -> AlarmRecord:
        """聚合告警
        
        Args:
            key: 告警类型和子类型的组合键
        
        Returns:
            AlarmRecord: 聚合后的告警记录
        """
        alerts = self.recent_alerts[key]
        if not alerts:
            return None
        
        # 获取第一个和最后一个告警
        first_alert = alerts[0]
        last_alert = alerts[-1]
        
        # 构建聚合消息
        alert_count = len(alerts)
        message = f"[{alert_count}次] {first_alert.message}"
        
        # 构建聚合详情
        details = {
            "original_alerts": [alert.dict() for alert in alerts],
            "first_timestamp": first_alert.timestamp.isoformat(),
            "last_timestamp": last_alert.timestamp.isoformat(),
            "alert_count": alert_count
        }
        
        # 创建聚合告警记录
        aggregated_alarm = AlarmRecord(
            alarm_type=first_alert.alarm_type,
            sub_type=first_alert.sub_type,
            severity=first_alert.severity,
            message=message,
            details=details
        )
        
        logger.info(f"聚合了 {alert_count} 个告警: {key}")
        return aggregated_alarm
    
    def _cleanup_old_alerts(self):
        """清理过期的告警记录"""
        now = datetime.now()
        for key, alerts in list(self.recent_alerts.items()):
            # 保留聚合窗口内的告警
            self.recent_alerts[key] = [
                alert for alert in alerts 
                if (now - alert.timestamp).total_seconds() < self.aggregation_window
            ]
            
            # 如果没有告警了，删除该键
            if not self.recent_alerts[key]:
                del self.recent_alerts[key]

# 创建全局告警聚合器实例
alarm_aggregator = AlarmAggregator()
