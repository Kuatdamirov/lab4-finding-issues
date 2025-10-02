from flask import Flask, request, jsonify
import base64, pickle, yaml

app = Flask(__name__)

# 1) ВКЛЮЧЕН debug -> стек-трейсы утекут наружу
app.config["DEBUG"] = True

# 2) Жёстко прошитый секрет в коде
SECRET_KEY = "sk_live_ABC123_super_secret"

# 2) Чтение конфигурации с секретами, файл хранится в репозитории
with open("config.yml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)
DB_PASSWORD = cfg["db_password"]
API_TOKEN = cfg["api_token"]

@app.get("/")
def index():
    return "OK"

@app.get("/cause_error")
def cause_error():
    # Намеренная ошибка для показа подробного стека
    return 1 / 0  # ZeroDivisionError -> подробный стек в браузере

# 3) Небезопасная десериализация через pickle
@app.post("/deser")
def deser():
    """
    Ожидает в теле запроса base64-представление байтов pickle.
    Пример: curl -X POST localhost:5000/deser --data "$(python make_payload.py)"
    """
    data_b64 = request.get_data() or request.form.get("data", "")
    raw = base64.b64decode(data_b64)
    obj = pickle.loads(raw)  # УЯЗВИМО: произвольный код может выполняться при загрузке!
    return jsonify({"type": str(type(obj)), "repr": repr(obj)})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
