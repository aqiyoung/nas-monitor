import React, { useEffect, useState } from 'react';
import api from '../utils/api';

interface AlarmRecord {
  id: string;
  alarm_type: string;
  sub_type: string;
  severity: string;
  message: string;
  details: any;
  timestamp: string;
  status: string;
  processed_at: string | null;
  processed_by: string | null;
}

interface AlarmConfig {
  id: string;
  alarm_type: string;
  sub_type: string;
  enabled: boolean;
  threshold: number;
  duration: number;
  severity: string;
  push_methods: string[];
  created_at: string;
  updated_at: string;
}

interface AccessIP {
  id: string;
  ip_address: string;
  country: string;
  region: string;
  city: string;
  is_blacklisted: boolean;
  first_seen: string;
  last_seen: string;
  total_requests: number;
}

const Alarm: React.FC = () => {
  const [alarmRecords, setAlarmRecords] = useState<AlarmRecord[]>([]);
  const [alarmConfigs, setAlarmConfigs] = useState<AlarmConfig[]>([]);
  const [accessIPs, setAccessIPs] = useState<AccessIP[]>([]);
  const [activeTab, setActiveTab] = useState<'records' | 'configs' | 'accessIPs'>('records');
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchData();
  }, [activeTab]);

  const fetchData = async () => {
    try {
      // 只在数据为空时设置loading为true（初始加载）
      const shouldShowLoading = 
        (activeTab === 'records' && alarmRecords.length === 0) ||
        (activeTab === 'configs' && alarmConfigs.length === 0) ||
        (activeTab === 'accessIPs' && accessIPs.length === 0);
      
      if (shouldShowLoading) {
        setLoading(true);
      }
      
      if (activeTab === 'records') {
        const response = await api.get('/api/alarm/records');
        setAlarmRecords(response.data);
      } else if (activeTab === 'configs') {
        const response = await api.get('/api/alarm/configs');
        setAlarmConfigs(response.data);
      } else if (activeTab === 'accessIPs') {
        const response = await api.get('/api/alarm/access-ips');
        setAccessIPs(response.data);
      }
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdate = async (recordId: string, status: string) => {
    try {
      await api.put(`/api/alarm/records/${recordId}`, { status });
      fetchData();
    } catch (error) {
      console.error('Failed to update alarm status:', error);
    }
  };

  const handleConfigToggle = async (configId: string, enabled: boolean) => {
    try {
      await api.put(`/api/alarm/configs/${configId}`, { enabled });
      fetchData();
    } catch (error) {
      console.error('Failed to toggle alarm config:', error);
    }
  };

  const handleIPBlacklistToggle = async (ipAddress: string, isBlacklisted: boolean) => {
    try {
      await api.put(`/api/alarm/access-ips/${ipAddress}`, { is_blacklisted: isBlacklisted });
      fetchData();
    } catch (error) {
      console.error('Failed to toggle IP blacklist:', error);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'red';
      case 'warning':
        return 'yellow';
      case 'info':
        return 'blue';
      default:
        return 'gray';
    }
  };

  return (
    <div className="container">
      <h1 className="page-title">告警管理</h1>
      
      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'records' ? 'active' : ''}`}
          onClick={() => setActiveTab('records')}
        >
          告警记录
        </button>
        <button 
          className={`tab ${activeTab === 'configs' ? 'active' : ''}`}
          onClick={() => setActiveTab('configs')}
        >
          告警配置
        </button>
        <button 
          className={`tab ${activeTab === 'accessIPs' ? 'active' : ''}`}
          onClick={() => setActiveTab('accessIPs')}
        >
          访问IP管理
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'records' && (
          <div className="card">
            <h2>告警记录</h2>
            {/* 只在初始加载时显示loading，数据刷新时不显示 */}
            {loading ? (
              <div className="loading-overlay">加载中...</div>
            ) : (
              <div className="alarm-records">
                {alarmRecords.length === 0 ? (
                  <div className="empty-state">
                    <i className="fas fa-bell-slash"></i>
                    <p>暂无告警记录</p>
                  </div>
                ) : (
                  <table className="alarm-table">
                    <thead>
                      <tr>
                        <th>时间</th>
                        <th>类型</th>
                        <th>级别</th>
                        <th>消息</th>
                        <th>状态</th>
                        <th>操作</th>
                      </tr>
                    </thead>
                    <tbody>
                      {alarmRecords.map((record) => (
                        <tr key={record.id} className={`alarm-item severity-${record.severity}`}>
                          <td>{new Date(record.timestamp).toLocaleString()}</td>
                          <td>{record.alarm_type} - {record.sub_type}</td>
                          <td>
                            <span className={`severity-badge ${record.severity}`}>
                              {record.severity}
                            </span>
                          </td>
                          <td>{record.message}</td>
                          <td>{record.status}</td>
                          <td>
                            <div className="action-buttons">
                              {record.status === 'unprocessed' && (
                                <>
                                  <button 
                                    className="btn btn-primary"
                                    onClick={() => handleStatusUpdate(record.id, 'processed')}
                                  >
                                    标记已处理
                                  </button>
                                  <button 
                                    className="btn btn-secondary"
                                    onClick={() => handleStatusUpdate(record.id, 'ignored')}
                                  >
                                    忽略
                                  </button>
                                </>
                              )}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            )}
          </div>
        )}

        {activeTab === 'configs' && (
          <div className="card">
            <h2>告警配置</h2>
            {/* 只在初始加载时显示loading，数据刷新时不显示 */}
            {loading ? (
              <div className="loading-overlay">加载中...</div>
            ) : (
              <div className="alarm-configs">
                {alarmConfigs.length === 0 ? (
                  <div className="empty-state">
                    <i className="fas fa-cog"></i>
                    <p>暂无告警配置</p>
                  </div>
                ) : (
                  <table className="config-table">
                    <thead>
                      <tr>
                        <th>类型</th>
                        <th>阈值</th>
                        <th>持续时间</th>
                        <th>级别</th>
                        <th>状态</th>
                        <th>操作</th>
                      </tr>
                    </thead>
                    <tbody>
                      {alarmConfigs.map((config) => (
                        <tr key={config.id} className="config-item">
                          <td>{config.alarm_type} - {config.sub_type}</td>
                          <td>{config.threshold}</td>
                          <td>{config.duration}秒</td>
                          <td>{config.severity}</td>
                          <td>
                            <span className={`status-badge ${config.enabled ? 'enabled' : 'disabled'}`}>
                              {config.enabled ? '启用' : '禁用'}
                            </span>
                          </td>
                          <td>
                            <button 
                              className={`btn ${config.enabled ? 'btn-secondary' : 'btn-primary'}`}
                              onClick={() => handleConfigToggle(config.id, !config.enabled)}
                            >
                              {config.enabled ? '禁用' : '启用'}
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            )}
          </div>
        )}

        {activeTab === 'accessIPs' && (
          <div className="card">
            <h2>访问IP管理</h2>
            {/* 只在初始加载时显示loading，数据刷新时不显示 */}
            {loading ? (
              <div className="loading-overlay">加载中...</div>
            ) : (
              <div className="access-ips">
                {accessIPs.length === 0 ? (
                  <div className="empty-state">
                    <i className="fas fa-network-wired"></i>
                    <p>暂无访问IP记录</p>
                  </div>
                ) : (
                  <table className="ip-table">
                    <thead>
                      <tr>
                        <th>IP地址</th>
                        <th>国家</th>
                        <th>地区</th>
                        <th>城市</th>
                        <th>请求次数</th>
                        <th>状态</th>
                        <th>最后访问</th>
                        <th>操作</th>
                      </tr>
                    </thead>
                    <tbody>
                      {accessIPs.map((ip) => (
                        <tr key={ip.id} className={`ip-item ${ip.is_blacklisted ? 'blacklisted' : ''}`}>
                          <td>{ip.ip_address}</td>
                          <td>{ip.country}</td>
                          <td>{ip.region}</td>
                          <td>{ip.city}</td>
                          <td>{ip.total_requests}</td>
                          <td>
                            <span className={`status-badge ${ip.is_blacklisted ? 'blacklisted' : 'whitelisted'}`}>
                              {ip.is_blacklisted ? '黑名单' : '白名单'}
                            </span>
                          </td>
                          <td>{new Date(ip.last_seen).toLocaleString()}</td>
                          <td>
                            <button 
                              className={`btn ${ip.is_blacklisted ? 'btn-secondary' : 'btn-primary'}`}
                              onClick={() => handleIPBlacklistToggle(ip.ip_address, !ip.is_blacklisted)}
                            >
                              {ip.is_blacklisted ? '移除黑名单' : '加入黑名单'}
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Alarm;
