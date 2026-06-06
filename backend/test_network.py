import socket

# 直接测试 TCP 连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('127.0.0.1', 5000))
    print("✓ 成功连接到端口 5000")
    
    # 发送 HTTP POST 请求
    request_data = b"POST /api/knowledge-points HTTP/1.1\r\nHost: 127.0.0.1:5000\r\nContent-Type: application/json\r\nContent-Length: 44\r\n\r\n{\"question\":\"test\",\"priority\":\"normal\",\"items\":[]}"
    s.send(request_data)
    
    # 接收响应
    response = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        response += chunk
    
    print(f"响应状态行: {response[:100]}")
    print(f"响应长度: {len(response)} bytes")
    
except Exception as e:
    print(f"连接失败: {e}")
finally:
    s.close()
