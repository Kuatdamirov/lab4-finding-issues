from flask import Flask, request, jsonify
import os, json, logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Прод-режим: без подробных ошибок наружу
app.config["DEBUG"] = False

# Секреты только из окружения (а не из git)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-not-set")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
API_TOKEN   = os.getenv("API_TOKEN", "")

# Лаконичный 500-ответ, подробности только в логах
logging.basicConfig(level=logging.INFO)

@app.errorhandler(Exception)
def handle_any_error(e):
    app.logger.exception("Unhandled exception")
    return jsonify({"error": "Internal server error"}), 500

@app.get("/")
def index():
    return "OK"

@app.get("/cause_error")
def cause_error():
    # Оставляем для проверки обработчика ошибок
    return 1 / 0

# Безопасная «десериализация»: JSON + валидация
@app.post("/deser")
def deser():
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Bad JSON"}), 400

    if not isinstance(payload, dict) or "role" not in payload:
        return jsonify({"error": "Invalid payload"}), 400

    return jsonify({"ok": True, "role": payload["role"]})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
