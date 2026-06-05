from flask import Flask, request, render_template_string
import requests
import os
import json

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
LINE_API = "https://api.line.me/v2/bot/message/reply"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_TOKEN}" if LINE_TOKEN else ""
}


def reply(reply_token, messages):
    if not LINE_TOKEN:
        print("LINE_TOKEN missing")
        return

    try:
        requests.post(
            LINE_API,
            headers=headers,
            data=json.dumps({"replyToken": reply_token, "messages": messages}),
            timeout=5
        )
    except Exception as e:
        print("reply error:", e)


# =========================
# 🍜 店家（簡化版）
# =========================
places = [
    "栄次郎燒肉", "FlagPasta", "小食。候", "義匠湯麵",
    "鄉親小吃", "逸麵鍋燒", "is pasta", "吉飽早餐"
]


# =========================
# LINE webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    try:
        body = request.get_json()
        if not body or "events" not in body:
            return "OK"

        event = body["events"][0]
        if "message" not in event:
            return "OK"

        msg = event["message"].get("text", "")
        reply_token = event.get("replyToken")

        if not reply_token:
            return "OK"

        # 🎡 轉盤入口（會員判斷）
        if msg == "美食轉盤":
            reply(reply_token, [
                {
                    "type": "template",
                    "altText": "會員功能",
                    "template": {
                        "type": "buttons",
                        "title": "會員功能",
                        "text": "此為會員功能",
                        "actions": [
                            {
                                "type": "uri",
                                "label": "我是會員",
                                "uri": "https://food-roulette-bot.onrender.com/roulette"
                            },
                            {
                                "type": "uri",
                                "label": "我不是會員",
                                "uri": "https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform?usp=header"
                            }
                        ]
                    }
                }
            ])

        # 🗺️ 地圖
        elif msg == "美食地圖":
            reply(reply_token, [{
                "type": "text",
                "text": "🗺️ https://food-roulette-bot.onrender.com/map"
            }])

        else:
            reply(reply_token, [{"type": "text", "text": "收到：" + msg}])

        return "OK"

    except Exception as e:
        print("webhook error:", e)
        return "OK"


# =========================
# 🎡 會員轉盤頁
# =========================
@app.route("/roulette")
def roulette():
    html = """
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>轉盤</title>
    <style>
    body{font-family:Arial;text-align:center;background:#fff3e6;}
    .box{margin-top:50px;}
    button{
        padding:15px 25px;
        font-size:18px;
        border:none;
        border-radius:10px;
        background:#ff6b6b;
        color:white;
    }
    </style>
    </head>
    <body>

    <div class="box">
        <h2>🎡 美食轉盤</h2>
        <p id="result">點擊開始</p>
        <button onclick="spin()">開始</button>
    </div>

    <script>
    const places = %s;

    function spin(){
        const pick = places[Math.floor(Math.random()*places.length)];
        document.getElementById("result").innerText = "👉 " + pick;
    }
    </script>

    </body>
    </html>
    """ % json.dumps(places, ensure_ascii=False)

    return render_template_string(html)


# =========================
# 🗺️ 地圖
# =========================
@app.route("/map")
def map_page():
    return """
    <h2>🗺️ 美食地圖</h2>
    <p>文化 / 陽明 / 幸福 / 新海</p>
    """


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
