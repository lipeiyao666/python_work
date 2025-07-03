import socket
import threading
import sys

def receive_msg(client_socket):
    """接收消息线程"""
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                print("与服务器断开连接")
                break
            print(f"\n{data}")
            print("请输入消息（格式：接收者:消息内容）：", end='', flush=True)
        except Exception as e:
            print(f"接收消息出错：{e}")
            break

def main():
    # 创建客户端socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 连接服务器
        client_socket.connect(('127.0.0.1', 8888))
        print("已连接到服务器，请登录")
        
        # 登录过程
        while True:
            username = input("请输入用户名：")
            password = input("请输入密码：")
            # 发送登录信息
            client_socket.send(f"login:{username}:{password}".encode('utf-8'))
            # 接收登录结果
            result = client_socket.recv(1024).decode('utf-8')
            print(result)
            if result == "登录成功":
                break
    
    # 启动消息接收线程
        threading.Thread(target=receive_msg, args=(client_socket,), daemon=True).start()
    
    # 消息发送循环
        while True:
            msg = input("请输入消息（格式：接收者:消息内容，输入exit退出）：")
            if msg.lower() == 'exit':
                break
            client_socket.send(msg.encode('utf-8'))
    
    except Exception as e:
        print(f"发生错误：{e}")
    finally:
        client_socket.close()
        print("已断开连接")

if __name__ == "__main__":
    main()