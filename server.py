import socket
import threading
import json
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 10000))

clients = []

def handle_client(conn, addr):
    print(f"🔥 연결됨: {addr}")
    clients.append(conn)

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            print("📨 메시지 수신")

            for c in clients:
                try:
                    c.send(data)
                except:
                    pass

    except:
        pass

    finally:
        print(f"❌ 연결 종료: {addr}")
        clients.remove(conn)
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"🚀 서버 실행됨 {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()