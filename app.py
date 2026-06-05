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
# 🗺️ 完整店家資料（含分區 + 連結）
# =========================
places = [
    {"name":"栄次郎燒肉","area":"文化","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
    {"name":"FlagPasta","area":"陽明","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
    {"name":"小食。候","area":"陽明","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
    {"name":"義匠湯麵","area":"陽明","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
    {"name":"鄉親小吃","area":"幸福","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
    {"name":"逸麵鍋燒","area":"新海","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
    {"name":"is pasta","area":"文化","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"},
    {"name":"吉飽早餐","area":"文化","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
    {"name":"致理飯糰","area":"文化","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
    {"name":"小松拉麵","area":"陽明","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"}
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

        # 🎡 轉盤（會員）
        if msg == "美食轉盤":
            reply(reply_token, [{
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
            }])

        # 🗺️ 地圖
        elif msg == "美食地圖":
            reply(reply_token, [{
                "type": "uri",
                "altText": "美食地圖",
                "uri": "https://food-roulette-bot.onrender.com/map"
            }])

        else:
            reply(reply_token, [{"type":"text","text":"收到：" + msg}])

        return "OK"

    except Exception as e:
        print("webhook error:", e)
        return "OK"


# =========================
# 🎡 轉盤頁
# =========================
@app.route("/roulette")
def roulette():

    names = [p["name"] for p in places]

    html = """
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>轉盤</title>
    <style>
    body{font-family:Arial;text-align:center;background:#fff3e6;}
    .box{margin-top:60px;}
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
    """ % json.dumps(names, ensure_ascii=False)

    return render_template_string(html)


# =========================
# 🗺️ 完整地圖（左右版 + 分區）
# =========================
@app.route("/map")
def map_page():

    html = """
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>美食地圖</title>

    <style>
    body{margin:0;font-family:Arial;background:#f7f3ea;}
    .wrap{display:flex;height:100vh;}

    .left{
        width:340px;
        overflow:auto;
        background:#fff8ee;
        padding:10px;
    }

    .card{
        background:white;
        margin:8px 0;
        padding:10px;
        border-radius:10px;
    }

    .right{
        flex:1;
        display:flex;
        flex-wrap:wrap;
        padding:10px;
        background:#f1eadf;
    }

    .area{
        width:45%;
        margin:10px;
        background:white;
        padding:10px;
        border-radius:12px;
    }

    @media(max-width:768px){
        .wrap{flex-direction:column;}
        .left{width:100%;height:40vh;}
        .right{height:60vh;}
    }
    </style>

    </head>

    <body>

    <div class="wrap">

    <div class="left">
    <h3>🍜 店家清單</h3>
    """

    for p in places:
        html += f"""
        <div class="card">
            <b>{p['name']}</b><br>
            🧭 {p['area']}<br>
            📍 <a href="{p['url']}" target="_blank">Google Maps</a>
        </div>
        """

    html += """
    </div>

    <div class="right">

    <div class="area">
    <h4>文化路</h4>
    栄次郎燒肉<br>is pasta<br>吉飽早餐<br>致理飯糰
    </div>

    <div class="area">
    <h4>陽明街</h4>
    FlagPasta<br>小食。候<br>義匠湯麵<br>小松拉麵
    </div>

    <div class="area">
    <h4>幸福路</h4>
    鄉親小吃
    </div>

    <div class="area">
    <h4>新海路</h4>
    逸麵鍋燒
    </div>

    </div>

    </div>

    </body>
    </html>
    """

    return render_template_string(html)


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
