from flask import Flask, request, render_template_string
import requests
import os
import json
from collections import defaultdict

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
# 🍜 店家資料
# =========================
places = [
    {"name":"栄次郎個人燒肉—板橋文化店","address":"文化路一段325號","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
    {"name":"FlagPasta","address":"陽明街23巷5號","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
    {"name":"小食。候","address":"陽明街23巷13號","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
    {"name":"義匠義式湯麵","address":"陽明街32號","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
    {"name":"鄉親小吃","address":"幸福路16號","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
    {"name":"逸麵鍋燒","address":"新海路101號","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
    {"name":"is pasta","address":"文化路一段321號2樓","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"},
    {"name":"吉飽早餐","address":"文化路一段311-19號","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
    {"name":"致理飯糰","address":"文化路一段311巷24號","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
    {"name":"小松拉麵","address":"自由路33號","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"}
]


# =========================
# 🚨 避免 map 404（重點修復）
# =========================
@app.route("/map")
def map_fix():
    return "📍 地圖功能已移除，請使用 /list 查看美食清單"


# =========================
# LINE webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()

    if not body or "events" not in body:
        return "OK"

    event = body["events"][0]
    msg = event.get("message", {}).get("text", "")
    reply_token = event.get("replyToken")

    if not reply_token:
        return "OK"

    # 🎡 轉盤
    if msg == "美食轉盤":
        reply(reply_token, [{
            "type": "template",
            "altText": "會員功能",
            "template": {
                "type": "buttons",
                "title": "會員功能",
                "text": "請選擇",
                "actions": [
                    {"type":"uri","label":"我是會員","uri":"https://food-roulette-bot.onrender.com/roulette"},
                    {"type":"uri","label":"我不是會員","uri":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform"}
                ]
            }
        }])

    # 📍 清單
    elif msg == "美食清單":
        reply(reply_token, [{
            "type":"uri",
            "altText":"美食清單",
            "uri":"https://food-roulette-bot.onrender.com/list"
        }])

    # 🗺️ 舊指令相容（避免老師按到壞掉）
    elif msg == "美食地圖":
        reply(reply_token, [{
            "type":"text",
            "text":"📍 地圖功能已改版，請點「美食清單」"
        }])

    else:
        reply(reply_token, [{"type":"text","text":"收到：" + msg}])

    return "OK"


# =========================
# 🎡 轉盤（不動）
# =========================
@app.route("/roulette")
def roulette():

    names = [p["name"] for p in places]

    html = """
    <html>
    <head><meta charset="utf-8"></head>
    <body style="text-align:center;font-family:Arial;background:#fff3e6;">
    <h2>🎡 美食轉盤</h2>
    <p id="r">點開始</p>
    <button onclick="spin()">開始</button>

    <script>
    const data = %s;
    function spin(){
        document.getElementById("r").innerText =
        "👉 " + data[Math.floor(Math.random()*data.length)];
    }
    </script>
    </body>
    </html>
    """ % json.dumps(names, ensure_ascii=False)

    return render_template_string(html)


# =========================
# 📍 清單（簡化版）
# =========================
@app.route("/list")
def list_page():

    grouped = defaultdict(list)

    for p in places:
        if "文化" in p["address"]:
            grouped["文化路"].append(p)
        elif "陽明" in p["address"]:
            grouped["陽明街"].append(p)
        elif "新海" in p["address"]:
            grouped["新海路"].append(p)
        elif "幸福" in p["address"]:
            grouped["幸福路"].append(p)
        else:
            grouped["其他"].append(p)

    html = """
    <html>
    <head>
    <meta charset="utf-8">
    <title>美食清單</title>
    <style>
    body{font-family:Arial;background:#f7f3ea;margin:0;}
    .wrap{padding:15px;}
    .block{background:white;margin:10px 0;padding:10px;border-radius:12px;}
    .item{padding:6px 0;border-bottom:1px solid #eee;}
    a{color:#ff5c5c;text-decoration:none;}
    </style>
    </head>
    <body>
    <div class="wrap">
    <h2>🍜 美食清單（分路）</h2>
    """

    for road, items in grouped.items():
        html += f"<div class='block'><h3>📍 {road}</h3>"
        for p in items:
            html += f"""
            <div class="item">
                <b>{p['name']}</b><br>
                📌 {p['address']}<br>
                🔗 <a href="{p['url']}" target="_blank">Google Maps</a>
            </div>
            """
        html += "</div>"

    html += "</div></body></html>"

    return render_template_string(html)


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
