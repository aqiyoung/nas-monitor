from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "NAS Monitor"
    APP_VERSION: str = "1.1.1"
    DEBUG: bool = False
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8017
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./nas_monitor.db"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # InfluxDB配置
    INFLUXDB_URL: str = "http://localhost:8086"
    INFLUXDB_TOKEN: str = ""
    INFLUXDB_ORG: str = "nas_monitor"
    INFLUXDB_BUCKET: str = "nas_metrics"
    
    # Prometheus配置
    PROMETHEUS_URL: str = "http://localhost:9090"
    
    # 告警配置
    ALARM_CHECK_INTERVAL: int = 60  # 秒
    
    # 邮件告警配置
    SMTP_SERVER: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    ALARM_EMAIL: str = ""
    
    # 钉钉告警配置
    DINGTALK_WEBHOOK: str = ""
    DINGTALK_SECRET: Optional[str] = None
    
    # 企业微信告警配置
    WEWORK_CORP_ID: str = ""
    WEWORK_AGENT_ID: str = ""
    WEWORK_APP_SECRET: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
