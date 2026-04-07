from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import os

app = FastAPI()

clients: list[WebSocket] = []


@app.get("/")
async def home():
    return {"status": "ok", "message": "HOTBURGER WEBSOCKET SERVER LIVE"}


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    print("🔥 웹소켓 연결됨")

    try:
        while True:
            data = await ws.receive_text()
            print("📨 메시지 수신:", data)

            dead = []
            for client in clients:
                try:
                    await client.send_text(data)
                except Exception:
                    dead.append(client)

            for d in dead:
                if d in clients:
                    clients.remove(d)

    except WebSocketDisconnect:
        print("❌ 웹소켓 연결 종료")
        if ws in clients:
            clients.remove(ws)
