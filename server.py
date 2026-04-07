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

        if secret != SECRET:
            return jsonify({"ok": False, "error": "unauthorized"}), 401

        if not text:
            return jsonify({"ok": False, "error": "empty text"}), 400

        MESSAGES.append(text)

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

        for idx, text in enumerate(MESSAGES):
            if idx > after:
                items.append({"id": idx, "text": text})

        return jsonify({"ok": True, "items": items})

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
