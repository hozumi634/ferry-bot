from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

ACCESS_TOKEN = "u8HVoZLtKf4hKDsGYshkuCuty5QK1Fvk8kQyVdq5YGo0b1F89fKqTa547BrWbCvaeO3h4LxewsIlQHCUpJ87EVP+ds0qw0UQhfir/g/OAq4lVHpf+VwQCUVXqp+F7hDaSc7VZ3xWDKaiSnR2jGby7AdB04t89/1O/w1cDnyilFU="

# 竹原 → 大崎上島
takehara = [
("06:05","垂水"),("06:35","白水"),("06:55","白水"),("07:25","垂水"),
("07:45","白水"),("08:05","垂水"),("08:25","垂水"),("09:00","白水"),
("09:25","垂水"),("09:55","白水"),("10:10","白水"),("10:40","垂水"),
("11:05","白水"),("12:05","白水"),("12:30","垂水"),("12:55","白水"),
("13:30","垂水"),("14:00","白水"),("14:25","垂水"),("15:00","白水"),
("15:25","垂水"),("15:45","白水"),("16:15","垂水"),("16:50","白水"),
("17:15","垂水"),("17:40","白水"),("18:00","白水"),("18:45","白水"),
("19:10","垂水"),("20:00","垂水"),("20:30","白水"),("21:30","白水")
]

# 上島 → 竹原
kamijima = [
("06:00","白水"),("06:30","垂水"),("06:55","垂水"),
("07:10","白水"),("07:30","白水※垂水経由"),("07:35","垂水※経由"),
("07:55","垂水"),("08:15","白水"),("08:35","垂水"),
("08:55","垂水"),("09:35","白水"),("09:55","垂水"),
("10:30","白水"),("11:10","垂水"),("11:30","白水"),
("12:20","白水"),("13:00","垂水"),("13:30","白水"),
("14:00","垂水"),("14:35","白水"),("14:55","垂水"),
("15:35","白水※垂水経由"),("15:40","垂水※経由"),
("15:55","垂水"),("16:15","白水"),("16:45","垂水"),
("17:05","白水"),("17:25","白水"),("17:45","垂水"),
("18:10","白水"),("18:35","白水※垂水経由"),
("18:40","垂水※経由"),("19:35","垂水"),
("20:00","白水"),("21:05","垂水")
]

def find_next(now, data):
    for t, port in data:
        if t > now:
            return t, port
    return data[0]

def minutes_diff(now_str, target_str):
    fmt = "%H:%M"
    now = datetime.strptime(now_str, fmt)
    target = datetime.strptime(target_str, fmt)
    diff = (target - now).total_seconds() / 60
    if diff < 0:
        diff += 24*60
    return int(diff)

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    events = body["events"]

    for event in events:
        reply_token = event["replyToken"]
        text = event["message"]["text"]

        now = datetime.now().strftime("%H:%M")

        # 判定
        if "竹原" in text:
            t, port = find_next(now, takehara)
            diff = minutes_diff(now, t)
            msg = f"次は {t}発（{port}行き）です。あと約{diff}分"
        else:
            t, port = find_next(now, kamijima)
            diff = minutes_diff(now, t)
            msg = f"次は {t}発（{port}発）です。あと約{diff}分"

        # LINEに返信
        requests.post( "https://api.line.me/v2/bot/message/reply", headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
            json={"replyToken": reply_token,"messages":[{"type":"text","text":msg}] } )

    return "OK"
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


