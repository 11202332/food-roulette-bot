from flask import Flask, request, render_template_string
import requests
import os
import json

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
LINE_API = "https://api.line.me/v2/bot/message/reply"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_TOKEN}"
}

def reply(reply_token, messages):
    if not LINE_TOKEN:
        print("LINE_TOKEN missing")
        return

    requests.post(
        LINE_API,
        headers=headers,
        data=json.dumps({
            "replyToken": reply_token,
            "messages": messages
        })
    )


# =========================
# 🍜 店家資料（你原本那份）
# =========================
places = [
    {"name":"栄次郎個人燒肉","rating":4.7,"price":"$200-400","type":"燒肉","comment":"自己烤肉很爽但錢包會痛"},
    {"name":"FlagPasta","rating":4.5,"price":"$200-400","type":"義大利麵","comment":"穩定不踩雷"},
    {"name":"小食。候","rating":4.3,"price":"$200-400","type":"咖啡","comment":"安靜但容易客滿"},
    {"name":"義匠義式湯麵","rating":4.8,"price":"$200-400","type":"義大利麵","comment":"湯麵很特別"},
    {"name":"鄉親小吃","rating":4.6,"price":"$1-200","type":"小吃","comment":"便宜實在"},
    {"name":"逸麵鍋燒","rating":4.9,"price":"$1-200","type":"鍋燒","comment":"湯頭超強"},
]


# =========================
# LINE webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()

    event = body["events"][0]
    msg = event["message"]["text"]
    reply_token = event["replyToken"]

    # 🎡 轉盤（完全保留你原本）
    if msg == "美食轉盤":
        reply(reply_token, [
            {"type":"text","text":"🎡 轉盤功能"},
            {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
        ])

    # 🗺️ 地圖（改成直接 HTML，不會 404）
    elif msg == "美食地圖":

        html = """
        <html>
        <head><meta charset="utf-8"><title>美食清單</title></head>
        <body style="font-family:Arial;padding:20px;">
        <h2>🍜 致理美食清單</h2>
        """

        for p in places:
            html += f"""
            <div style="margin-bottom:10px;padding:10px;border:1px solid #ddd;">
                <b>{p['name']}</b><br>
                ⭐ {p['rating']} | {p['price']}<br>
                {p['comment']}
            </div>
            """

        html += "</body></html>"

        reply(reply_token, [{
            "type": "text",
            "text": "👉 https://food-roulette-bot.onrender.com/map"
        }])

    else:
        reply(reply_token, [{"type":"text","text":"收到：" + msg}])

    return "OK"


# =========================
# 🗺️ map（重點修正）
# =========================
@app.route("/map")
def map_page():
    return render_template_string("""
    <html>
    <head><meta charset="utf-8"><title>美食清單</title></head>
    <body style="font-family:Arial;padding:20px;">
        <h2>🍜 美食清單</h2>
        {% for p in places %}
        <div style="margin-bottom:10px;padding:10px;border:1px solid #ddd;">
            <b>{{p.name}}</b><br>
            ⭐ {{p.rating}} | {{p.price}}<br>
            {{p.comment}}
        </div>
        {% endfor %}
    </body>
    </html>
    """, places=places)


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
