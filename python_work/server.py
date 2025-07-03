import socket
import threading

# 存储已登录用户信息：用户名 -> 客户端socket
users = {}
# 预设用户信息（用户名:密码）
user_info = {
    "user1": "123456",
    "user2": "654321"
}

def handle_client(client_socket):
    """处理客户端连接"""
    username = None
    try:
        # 登录验证
        while True:
            # 接收客户端发送的用户名和密码
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            
            # 解析登录信息（格式："login:用户名:密码"）
            if data.startswith("login:"):
                _, user, pwd = data.split(':')
                if user in user_info and user_info[user] == pwd:
                    # 检查是否已登录
                    if user in users:
                        client_socket.send("该用户已登录".encode('utf-8'))
                    else:
                        username = user
                        users[username] = client_socket
                        client_socket.send("登录成功".encode('utf-8'))
                        print(f"{username} 登录成功")
                        break
                else:
                    client_socket.send("用户名或密码错误".encode('utf-8'))
        
        # 消息转发
        if username:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                # 解析消息（格式："接收者:消息内容"）
                if ':' in data:
                    receiver, msg = data.split(':', 1)
                    if receiver in users:
                        # 转发消息给接收者
                        users[receiver].send(f"{username}说：{msg}".encode('utf-8'))
                        # 发送成功反馈
                        client_socket.send("消息已发送".encode('utf-8'))
                    else:
                        client_socket.send(f"用户{receiver}不在线".encode('utf-8'))
                else:
                    client_socket.send("消息格式错误，请使用'接收者:消息内容'".encode('utf-8'))
    
    except Exception as e:
        print(f"处理{username}时出错：{e}")
    finally:
        # 清理连接
        if username in users:
            del users[username]
            print(f"{username} 已下线")
        client_socket.close()

def main():
    # 创建TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定地址和端口
    server_socket.bind(('127.0.0.1', 8888))
    # 监听连接（最大5个等待连接）
    server_socket.listen(5)
    print("服务器已启动，等待连接...")
    
    try:
        while True:
            # 接受客户端连接
            client_socket, client_addr = server_socket.accept()
            print(f"收到来自{client_addr}的连接")
            
            # 创建线程处理客户端
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("服务器关闭")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()