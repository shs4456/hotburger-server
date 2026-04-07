from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

clients = set()


@app.route("/")
def home():
    return "HOTBURGER WebSocket Server Alive"


@sock.route("/ws")
def websocket(ws):
    clients.add(ws)
    print("클라이언트 연결됨:", len(clients))

    try:
        while True:
            data = ws.receive()

            if data is None:
                break
            print("메시지 수신:", str(data)[:50])

            # 클라이언트 keepalive 용도
            if data in ("__hello__", "__ping__"):
                continue

            dead = []
            for c in list(clients):
                if c is ws:
                    continue
                try:
                    c.send(data)
                except:
                    dead.append(c)

            for d in dead:
                try:
                    clients.remove(d)
                except:
                    pass

    except Exception as e:
        print("에러:", e)

    finally:
        try:
            clients.remove(ws)
        except:
            pass

        print("연결 종료:", len(clients))
