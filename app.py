from flask import Flask, request, render_template_string
import requests
import os
import json
import random

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
LINE_API = "https://api.line.me/v2/bot/message/reply"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_TOKEN}"
}

def reply(reply_token, messages):
    payload = {
        "replyToken": reply_token,
        "messages": messages
    }
    requests.post(LINE_API, headers=headers, data=json.dumps(payload))


# =========================
# 🍜 店家資料
# =========================
places = [
    {"name":"栄次郎個人燒肉—板橋文化店","address":"文化路一段325號","rating":"4.7","price":"$200-400","time":"11:30-23:30","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
    {"name":"FlagPasta","address":"陽明街23巷5號","rating":"4.5","price":"$200-400","time":"11:00-21:00","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
    {"name":"小食。候","address":"陽明街23巷13號","rating":"4.3","price":"$200-400","time":"12:00-19:00","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
    {"name":"義匠義式湯麵","address":"陽明街32號","rating":"4.8","price":"$200-400","time":"11:30-21:00","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
    {"name":"鄉親小吃","address":"幸福路16號","rating":"4.6","price":"$1-200","time":"11:00-19:00","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
    {"name":"台南無刺虱目魚","address":"新海路97號","rating":"4.4","price":"$1-200","time":"11:00-22:00","url":"https://maps.app.goo.gl/7b41uvR3Bimf2iGR8"},
    {"name":"逸麵麵鍋燒","address":"新海路101號","rating":"4.9","price":"$1-200","time":"11:30-21:00","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
    {"name":"is pasta","address":"文化路一段321號2樓","rating":"4.3","price":"$200-400","time":"11:20-21:15","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"},
    {"name":"吉飽早餐","address":"文化路一段311-19號","rating":"4.0","price":"$1-200","time":"7:00-14:00","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
    {"name":"太極鰲車輪餅","address":"漢生西路128號","rating":"4.3","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/xYUnsWEWp4qL1Mg48"},
    {"name":"小松拉麵","address":"自由路33號","rating":"4.5","price":"$1-200","time":"11:30-21:30","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"},
    {"name":"一京咖哩","address":"陽明街109號","rating":"4.6","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8"},
    {"name":"致理飯糰","address":"文化路一段311巷24號","rating":"4.7","price":"$1-200","time":"9:00-17:15","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
    {"name":"吳二麻辣鴨血","address":"文化路一段311之6號","rating":"4.4","price":"$1-200","time":"10:30-20:30","url":"https://maps.app.goo.gl/wTVnP3P1BeXfMweHA"},
    {"name":"吉野烤肉飯","address":"文化路一段311-15號","rating":"3.8","price":"$1-200","time":"10:30-20:00","url":"https://maps.app.goo.gl/4NuMrst9S6LaLsAAA"},
    {"name":"MABO POKE","address":"文化路一段311之3號","rating":"4.3","price":"$1-200","time":"11:00-20:30","url":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9"},
    {"name":"小陳滷社","address":"文化路一段311巷22號","rating":"3.9","price":"$1-200","time":"11:30-20:00","url":"https://maps.app.goo.gl/1hxJG1hFFHHWA8c69"},
    {"name":"Café Wanderer","address":"陽明街27巷7號","rating":"4.4","price":"$200-400","time":"10:00-20:30","url":"https://maps.app.goo.gl/fY6ryS1ZkMVXLkyC9"},
]


# =========================
# LINE webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()

    try:
        event = body["events"][0]
        msg = event["message"]["text"]
        reply_token = event["replyToken"]

        # 🎡 轉盤入口（會員判斷）
        if msg == "美食轉盤":
            reply(reply_token, [{
                "type":"template",
                "altText":"會員選擇",
                "template":{
                    "type":"buttons",
                    "text":"你是會員嗎？",
                    "actions":[
                        {"type":"message","label":"我是會員","text":"抽餐廳"},
                        {"type":"uri","label":"我不是會員",
                         "uri":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform?usp=header"}
                    ]
                }
            }])

        # 🎡 真轉盤
        elif msg == "抽餐廳":
            p = random.choice(places)

            reply(reply_token, [{
                "type":"text",
                "text": f"🎡 抽到：{p['name']}\n⭐ {p['rating']} | 💰 {p['price']}\n📍 {p['address']}"
            },
            {
                "type":"text",
                "text": p["url"]
            }])

        # 🗺️ 清單
        elif msg == "美食地圖":
            reply(reply_token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"打開美食清單",
                    "actions":[
                        {"type":"uri","label":"進入地圖",
                         "uri":"https://food-roulette-bot.onrender.com/map"}
                    ]
                }
            }])

        else:
            reply(reply_token, [{"type":"text","text":"收到：" + msg}])

        return "OK"

    except:
        return "OK"


# =========================
# 🗺️ 地圖頁（不卡 + 好看）
# =========================
@app.route("/map")
def map_page():
    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>美食清單</title>

<style>
body{
    margin:0;
    font-family:Arial;
    background:#fff6ed;
}

.container{
    max-width:800px;
    margin:auto;
    padding:20px;
}

.card{
    background:white;
    margin:12px 0;
    padding:14px;
    border-radius:16px;
    box-shadow:0 2px 8px rgba(0,0,0,0.1);
}

.name{
    font-size:18px;
    font-weight:bold;
}

a{
    display:inline-block;
    margin-top:8px;
    padding:8px 12px;
    background:#ff4d4d;
    color:white;
    border-radius:10px;
    text-decoration:none;
}
</style>
</head>

<body>
<div class="container">
<h2>🍜 致理美食清單</h2>
"""

    for p in places:
        html += f"""
        <div class="card">
            <div class="name">{p['name']}</div>
            ⭐ {p['rating']} | 💰 {p['price']}<br>
            🕒 {p['time']}<br>
            📍 {p['address']}<br>
            <a href="{p['url']}" target="_blank">開啟 Google Maps</a>
        </div>
        """

    html += """
</div>
</body>
</html>
"""
    return render_template_string(html)


# =========================
# home
# =========================
@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
