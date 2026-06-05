from flask import Flask, request, render_template_string, jsonify
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
    {"name":"栄次郎個人燒肉","address":"文化路一段325號","rating":"4.7","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
    {"name":"FlagPasta","address":"陽明街23巷5號","rating":"4.5","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
    {"name":"小食。候","address":"陽明街23巷13號","rating":"4.3","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
    {"name":"義匠義式湯麵","address":"陽明街32號","rating":"4.8","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
    {"name":"鄉親小吃","address":"幸福路16號","rating":"4.6","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
    {"name":"台南無刺虱目魚","address":"新海路97號","rating":"4.4","url":"https://maps.app.goo.gl/7b41uvR3Bimf2iGR8"},
    {"name":"逸麵麵鍋燒","address":"新海路101號","rating":"4.9","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
    {"name":"is pasta","address":"文化路321號2樓","rating":"4.3","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"},
    {"name":"吉飽早餐","address":"文化路311-19號","rating":"4.0","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
    {"name":"太極鰲車輪餅","address":"漢生西路128號","rating":"4.3","url":"https://maps.app.goo.gl/xYUnsWEWp4qL1Mg48"},
    {"name":"小松拉麵","address":"自由路33號","rating":"4.5","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"},
    {"name":"一京咖哩","address":"陽明街109號","rating":"4.6","url":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8"},
    {"name":"致理飯糰","address":"文化路311巷24號","rating":"4.7","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
    {"name":"吳二麻辣鴨血","address":"文化路311之6號","rating":"4.4","url":"https://maps.app.goo.gl/wTVnP3P1BeXfMweHA"},
    {"name":"吉野烤肉飯","address":"文化路311-15號","rating":"3.8","url":"https://maps.app.goo.gl/4NuMrst9S6LaLsAAA"},
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

        # 🎡 入口
        if msg == "美食轉盤":
            reply(reply_token, [{
                "type":"template",
                "altText":"轉盤",
                "template":{
                    "type":"buttons",
                    "text":"是否進入會員轉盤？",
                    "actions":[
                        {"type":"message","label":"我是會員","text":"進入轉盤"},
                        {"type":"uri","label":"我不是會員",
                         "uri":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform?usp=header"}
                    ]
                }
            }])

        # 🎡 進入轉盤頁
        elif msg == "進入轉盤":
            reply(reply_token, [{
                "type":"text",
                "text":"🎡 轉盤準備完成"
            },
            {
                "type":"text",
                "text":"https://food-roulette-bot.onrender.com/wheel"
            }])

        # 🗺️ 清單
        elif msg == "美食地圖":
            reply(reply_token, [{
                "type":"text",
                "text":"👇 打開美食清單"
            },
            {
                "type":"text",
                "text":"https://food-roulette-bot.onrender.com/map"
            }])

        else:
            reply(reply_token, [{"type":"text","text":"收到：" + msg}])

        return "OK"

    except:
        return "OK"


# =========================
# 🎡 轉盤 UI（完整動畫版）
# =========================
@app.route("/wheel")
def wheel():
    names = [p["name"] for p in places]

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>美食轉盤</title>

<style>
body {{
    margin:0;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    background:#fff3e6;
    font-family:Arial;
}}

#wheel {{
    width:420px;
    height:420px;
    border-radius:50%;
    border:10px solid #ff4d4d;
    position:relative;
    transition: transform 4s cubic-bezier(0.2, 0.8, 0.2, 1);
    overflow:hidden;
}}

.center {{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    font-weight:bold;
}}

#btn {{
    margin-top:20px;
    padding:10px 16px;
    background:#ff4d4d;
    color:white;
    border:none;
    border-radius:10px;
    cursor:pointer;
}}
</style>
</head>

<body>

<div style="text-align:center;">
    <div id="wheel">
        <div class="center">🎡</div>
    </div>

    <button id="btn">開始轉盤</button>
</div>

<script>
let names = {names};
let wheel = document.getElementById("wheel");

let angle = 360 / names.length;

document.getElementById("btn").onclick = async function() {{

    let index = Math.floor(Math.random() * names.length);
    let deg = 3600 + (index * angle);

    wheel.style.transform = "rotate(" + deg + "deg)";

    setTimeout(async () => {{
        let res = await fetch("/spin?i=" + index);
        let data = await res.json();

        alert(
            "🎉 抽到：" + data.name +
            "\\n📍 " + data.address +
            "\\n⭐ " + data.rating
        );
    }}, 4200);
}};
</script>

</body>
</html>
"""
    return render_template_string(html)


# =========================
# 🎯 抽結果 API
# =========================
@app.route("/spin")
def spin():
    i = int(request.args.get("i"))
    return jsonify(places[i])


# =========================
# 🗺️ 清單頁
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
<h2>🍜 美食清單</h2>
"""

    for p in places:
        html += f"""
        <div class="card">
            <b>{p['name']}</b><br>
            ⭐ {p['rating']}<br>
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
