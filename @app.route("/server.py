from flask import Flask, request, jsonify

app = Flask(__name__)

MESSAGES = []
MAX_MESSAGES = 500
SECRET = "hotburger123"

LATEST_BOARD_FEED = {
    "updated_at": "",
    "events": []
}
LATEST_BOARD_STARRED = {
    "updated_at": "",
    "items": []
}


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
# 보드 feed 저장
# =========================
@app.route("/board_feed_push", methods=["POST"])
def board_feed_push():
    try:
        data = request.get_json(force=True)
        secret = str(data.get("secret", ""))

        if secret != SECRET:
            return jsonify({"ok": False, "error": "unauthorized"}), 401

        feed = data.get("feed", {})
        if not isinstance(feed, dict):
            return jsonify({"ok": False, "error": "invalid feed"}), 400

        global LATEST_BOARD_FEED
        LATEST_BOARD_FEED = feed

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# =========================
# 보드 feed 조회
# =========================
@app.route("/board-feed", methods=["GET"])
def board_feed():
    try:
        return jsonify(LATEST_BOARD_FEED)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# =========================
# 보드 starred 저장
# =========================
@app.route("/board_starred_push", methods=["POST"])
def board_starred_push():
    try:
        data = request.get_json(force=True)
        secret = str(data.get("secret", ""))

        if secret != SECRET:
            return jsonify({"ok": False, "error": "unauthorized"}), 401

        starred = data.get("starred", {})
        if not isinstance(starred, dict):
            return jsonify({"ok": False, "error": "invalid starred"}), 400

        global LATEST_BOARD_STARRED
        LATEST_BOARD_STARRED = starred

        return jsonify({"ok": True})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
    

# =========================
# 보드 starred 조회
# =========================
@app.route("/board-starred", methods=["GET"])
def board_starred():
    try:
        return jsonify(LATEST_BOARD_STARRED)
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
