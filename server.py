from flask import Flask, request, jsonify

app = Flask(__name__)

MESSAGES = []
MAX_MESSAGES = 500
SECRET = "hotburger123"


@app.route("/")
def home():
    return "HOTBURGER SERVER OK"


@app.route("/push", methods=["POST"])
def push():
    try:
        data = request.get_json(force=True)
        secret = str(data.get("secret", ""))
        text = str(data.get("text", "")).strip()
        stock_name = str(data.get("stock_name", "")).strip()

        if secret != SECRET:
            return jsonify({"ok": False, "error": "unauthorized"}), 401

        if not text:
            return jsonify({"ok": False, "error": "empty text"}), 400

        MESSAGES.append({
            "text": text,
            "stock_name": stock_name,
        })

        if len(MESSAGES) > MAX_MESSAGES:
            del MESSAGES[:-MAX_MESSAGES]

        return jsonify({"ok": True, "count": len(MESSAGES)})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/pull", methods=["GET"])
def pull():
    try:
        after = int(request.args.get("after", "-1"))
        items = []

        for idx, item in enumerate(MESSAGES):
            if idx > after:
                items.append({
                    "id": idx,
                    "text": item.get("text", ""),
                    "stock_name": item.get("stock_name", ""),
                })

        return jsonify({"ok": True, "items": items})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# =========================
# 시장 데이터 저장
# =========================
MARKET_DATA = {}

@app.route("/market_push", methods=["POST"])
def market_push():
    try:
        data = request.get_json(force=True)
        secret = data.get("secret", "")

        if secret != SECRET:
            return jsonify({"ok": False, "error": "unauthorized"}), 401

        global MARKET_DATA
        MARKET_DATA = data.get("market", {})

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================
# 시장 데이터 조회
# =========================
@app.route("/market", methods=["GET"])
def market():
    try:
        return jsonify({
            "ok": True,
            "market": MARKET_DATA
        })

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
