import React, { useState, useEffect, useCallback } from 'react'
import { Button, Table, Modal, Form, Input, Switch, message, Space, Tooltip } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined, UserOutlined } from '@ant-design/icons'

interface User {
  id: string
  username: string
  hashed_password?: string
  disabled: boolean
  created_at: string
  updated_at: string
}

const UserManagement: React.FC = () => {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [visible, setVisible] = useState<boolean>(false)
  const [editingUser, setEditingUser] = useState<User | null>(null)
  const [form] = Form.useForm()

  // 获取用户列表
  const fetchUsers = useCallback(async () => {
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/user/', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setUsers(data)
      } else {
        throw new Error('Failed to fetch users')
      }
    } catch (error) {
      message.error('获取用户列表失败')
      console.error('Error fetching users:', error)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchUsers()
  }, [fetchUsers])

  // 打开添加/编辑模态框
  const showModal = (user: User | null = null) => {
    setEditingUser(user)
    if (user) {
      form.setFieldsValue({
        username: user.username,
        disabled: user.disabled
      })
    } else {
      form.resetFields()
    }
    setVisible(true)
  }

  // 关闭模态框
  const handleCancel = () => {
    setVisible(false)
    setEditingUser(null)
  }

  // 提交表单
  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()
      const token = localStorage.getItem('token')
      let response

      if (editingUser) {
        // 更新用户
        response = await fetch(`/api/user/${editingUser.username}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(values)
        })
      } else {
        // 创建用户
        response = await fetch('/api/user/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(values)
        })
      }

      if (response.ok) {
        message.success(editingUser ? '用户更新成功' : '用户创建成功')
        setVisible(false)
        fetchUsers()
        setEditingUser(null)
      } else {
        const errorData = await response.json()
        throw new Error(errorData.detail || '操作失败')
      }
    } catch (error: any) {
      message.error(error.message || '操作失败')
      console.error('Error submitting form:', error)
    }
  }

  // 删除用户
  const handleDelete = async (username: string) => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`/api/user/${username}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        message.success('用户删除成功')
        fetchUsers()
      } else {
        const errorData = await response.json()
        throw new Error(errorData.detail || '删除失败')
      }
    } catch (error: any) {
      message.error(error.message || '删除失败')
      console.error('Error deleting user:', error)
    }
  }

  return (
    <div className="user-management-container">
      <div className="header-section">
        <h2><UserOutlined /> 用户管理</h2>
        <Button 
          type="primary" 
          icon={<PlusOutlined />} 
          onClick={() => showModal()}
        >
          添加用户
        </Button>
      </div>

      <Table 
        dataSource={users} 
        loading={loading} 
        rowKey="username"
        pagination={{ pageSize: 10 }}
        className="user-table"
      >
        <Table.Column 
          title="用户名" 
          dataIndex="username" 
          key="username" 
        />
        <Table.Column 
          title="状态" 
          dataIndex="disabled" 
          key="disabled"
          render={(disabled) => (
            <span>{disabled ? '禁用' : '启用'}</span>
          )}
        />
        <Table.Column 
          title="创建时间" 
          dataIndex="created_at" 
          key="created_at"
          render={(createdAt) => new Date(createdAt).toLocaleString()}
        />
        <Table.Column 
          title="更新时间" 
          dataIndex="updated_at" 
          key="updated_at"
          render={(updatedAt) => new Date(updatedAt).toLocaleString()}
        />
        <Table.Column 
          title="操作" 
          key="action"
          render={(_, record) => (
            <Space size="middle">
              <Tooltip title="编辑">
                <Button 
                  type="primary" 
                  icon={<EditOutlined />} 
                  size="small"
                  onClick={() => showModal(record)}
                />
              </Tooltip>
              <Tooltip title="删除">
                <Button 
                  danger 
                  icon={<DeleteOutlined />} 
                  size="small"
                  onClick={() => handleDelete(record.username)}
                />
              </Tooltip>
            </Space>
          )}
        />
      </Table>

      {/* 添加/编辑用户模态框 */}
      <Modal
        title={editingUser ? '编辑用户' : '添加用户'}
        open={visible}
        onOk={handleSubmit}
        onCancel={handleCancel}
        okText="保存"
        cancelText="取消"
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{ disabled: false }}
        >
          <Form.Item
            name="username"
            label="用户名"
            rules={[{ required: true, message: '请输入用户名' }]}
          >
            <Input placeholder="请输入用户名" />
          </Form.Item>

          {!editingUser && (
            <Form.Item
              name="password"
              label="密码"
              rules={[{ required: true, message: '请输入密码' }]}
            >
              <Input.Password placeholder="请输入密码" />
            </Form.Item>
          )}

          <Form.Item
            name="disabled"
            label="状态"
            valuePropName="checked"
          >
            <Switch checkedChildren="启用" unCheckedChildren="禁用" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default React.memo(UserManagement)