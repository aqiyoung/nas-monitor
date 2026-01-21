from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.alarm.alarm_detector import alarm_detector
import time

class AlarmScheduler:
    """告警定时任务服务"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self._setup_jobs()
    
    def _setup_jobs(self):
        """设置定时任务"""
        # 每10秒运行一次告警检测
        self.scheduler.add_job(
            func=alarm_detector.run_detection,
            trigger=IntervalTrigger(seconds=10),
            id='alarm_detection_job',
            name='Run alarm detection every 10 seconds',
            replace_existing=True
        )
    
    def shutdown(self):
        """关闭调度器"""
        self.scheduler.shutdown()

# 创建全局定时任务实例
alarm_scheduler = AlarmScheduler()
