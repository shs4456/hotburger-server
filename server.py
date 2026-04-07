from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

clients = []

@app.route("/")
def home():
    return "HOTBURGER WebSocket Server Alive"

@sock.route("/ws")
def websocket(ws):
    clients.append(ws)
    print("클라이언트 연결됨")

    try:
        while True:
            data = ws.receive()

            if not data:
                break

            print("메시지 수신")

            for c in clients:
                try:
                    c.send(data)
                except:
                    pass

    except:
        pass

    finally:
        clients.remove(ws)
        print("연결 종료")
