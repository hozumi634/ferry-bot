from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

ACCESS_TOKEN = "u8HVoZLtKf4hKDsGYshkuCuty5QK1Fvk8kQyVdq5YGo0b1F89fKqTa547BrWbCvaeO3h4LxewsIlQHCUpJ87EVP+ds0qw0UQhfir/g/OAq4lVHpf+VwQCUVXqp+F7hDaSc7VZ3xWDKaiSnR2jGby7AdB04t89/1O/w1cDnyilFU="

takehara = [
    ("06:05","垂水"),("06:35","白水"),("15:00","白水"),("15:45","白水")
]

kamijima = [
    ("06:00","白水"),("06:30","垂水"),("15:40","垂水※経由"),("21:05","垂水")
]

def find_next(now, data):
    for t, port in data:
        if t > now:
            return t, port
    return data[0]

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    events = body["events"]

    for event in events:
        reply_token = event["replyToken"]
        text = event["message"]["text"]
        now = datetime.now().strftime("%H:%M")

        if "竹原" in text:
            t, port = find_next(now, takehara)
            msg = f"次は {t}発（{port}）"
        else:
            t, port = find_next(now, kamijima)
            msg = f"次は {t}発（{port}）"

        requests.post(
            "https://api.line.me/v2/bot/message/reply",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
            json={
                "replyToken": reply_token,
                "messages":[{"type":"text","text":msg}]
            }
        )
    return "OK"
