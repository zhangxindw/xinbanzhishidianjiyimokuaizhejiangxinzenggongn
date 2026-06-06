import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('127.0.0.1', 5000))
    
    # 发送 HTTP POST 请求
    json_data = '{"question":"test","priority":"normal","items":[]}'
    request_data = f"POST /api/knowledge-points HTTP/1.1\r\nHost: 127.0.0.1:5000\r\nContent-Type: application/json\r\nContent-Length: {len(json_data)}\r\n\r\n{json_data}"
    print(f"发送的请求:\n{request_data}")
    s.send(request_data.encode('utf-8'))
    
    # 接收响应
    response = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        response += chunk
    
    print(f"\n响应:\n{response.decode('utf-8')}")
    
except Exception as e:
    print(f"错误: {e}")
finally:
    s.close()
