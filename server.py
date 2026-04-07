from flask import Flask, request, jsonify
import time
import os

app = Flask(__name__)

messages = []
next_id = 1

@app.get("/")
def home():
    return "hotburger server alive", 200

@app.post("/push")
def push():
    global next_id

    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    stock = data.get("stock", "")
    sender = data.get("sender", "main")

    item = {
        "id": next_id,
        "ts": time.time(),
        "text": text,
        "stock": stock,
        "sender": sender,
    }
    next_id += 1
    messages.append(item)

    # 최근 200개만 유지
    if len(messages) > 200:
        del messages[:-200]

    return jsonify({"ok": True, "id": item["id"]})

@app.get("/poll")
def poll():
    after = request.args.get("after", default=0, type=int)
    items = [m for m in messages if m["id"] > after]
    return jsonify({"ok": True, "messages": items})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
