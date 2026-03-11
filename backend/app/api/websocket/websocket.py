from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
import uuid
from app.services.websocket.websocket_service import manager
import json

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str = Query(None)
):
    """WebSocket端点"""
    # 如果没有提供client_id，生成一个
    if not client_id:
        client_id = str(uuid.uuid4())
    
    # 接受连接
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            
            # 解析消息
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                if message_type == "subscribe":
                    # 订阅主题
                    topics = message.get("topics", [])
                    manager.subscribe(client_id, topics)
                    
                    # 发送确认消息
                    await websocket.send_json({
                        "type": "subscribed",
                        "topics": topics,
                        "client_id": client_id
                    })
                
                elif message_type == "unsubscribe":
                    # 取消订阅主题
                    topics = message.get("topics", [])
                    manager.unsubscribe(client_id, topics)
                    
                    # 发送确认消息
                    await websocket.send_json({
                        "type": "unsubscribed",
                        "topics": topics,
                        "client_id": client_id
                    })
                
                elif message_type == "ping":
                    # 心跳消息
                    await websocket.send_json({
                        "type": "pong",
                        "client_id": client_id
                    })
                
                else:
                    # 未知消息类型
                    await websocket.send_json({
                        "type": "error",
                        "message": "未知消息类型",
                        "client_id": client_id
                    })
            except json.JSONDecodeError:
                # 无效的JSON
                await websocket.send_json({
                    "type": "error",
                    "message": "无效的JSON格式",
                    "client_id": client_id
                })
    except WebSocketDisconnect:
        # 断开连接
        manager.disconnect(client_id)
    except Exception as e:
        # 其他错误
        print(f"WebSocket错误: {str(e)}")
        manager.disconnect(client_id)
