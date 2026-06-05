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
    payload = {
        "replyToken": reply_token,
        "messages": messages
    }
    requests.post(LINE_API, headers=headers, data=json.dumps(payload))


# =========================
# 🍜 店家資料（已擴充）
# =========================
places = [
    {"name":"栄次郎個人燒肉—板橋文化店","address":"文化路一段","rating":"4.7","price":"$200-400","time":"11:30-23:30","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
    {"name":"FlagPasta","address":"陽明街","rating":"4.5","price":"$200-400","time":"11:00-21:00","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
    {"name":"小食。候","address":"陽明街","rating":"4.3","price":"$200-400","time":"12:00-19:00","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
    {"name":"義匠義式湯麵","address":"陽明街","rating":"4.8","price":"$200-400","time":"11:30-21:00","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
    {"name":"鄉親小吃","address":"幸福路","rating":"4.6","price":"","time":"11:00-19:00","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},

    {"name":"台南虱目魚","address":"新海路","rating":"4.4","price":"$1-200","time":"11:00-22:00","url":"https://maps.app.goo.gl/7b41uvR3Bimf2iGR8"},
    {"name":"逸麵鍋燒","address":"新海路","rating":"4.9","price":"$1-200","time":"11:30-21:00","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
    {"name":"is pasta","address":"文化路","rating":"4.3","price":"$200-400","time":"11:20-21:15","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"},
    {"name":"吉飽早餐","address":"文化路","rating":"4.0","price":"$1-200","time":"07:00-14:00","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
    {"name":"太極鰲車輪餅","address":"漢生西路","rating":"4.3","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/xYUnsWEWp4qL1Mg48"},

    {"name":"小松拉麵","address":"自由路","rating":"4.5","price":"$1-200","time":"11:30-21:30","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"},
    {"name":"一京咖哩","address":"陽明街","rating":"4.6","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8"},
    {"name":"致理飯糰","address":"文化路","rating":"4.7","price":"$1-200","time":"09:00-17:15","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
    {"name":"吳二麻辣鴨血","address":"文化路","rating":"4.4","price":"$1-200","time":"10:30-20:30","url":"https://maps.app.goo.gl/wTVnP3P1BeXfMweHA"},
    {"name":"吉野烤肉飯","address":"文化路","rating":"3.8","price":"$1-200","time":"10:30-20:00","url":"https://maps.app.goo.gl/4NuMrst9S6LaLsAAA"},

    {"name":"MABO POKE","address":"文化路","rating":"4.3","price":"$1-200","time":"11:00-20:30","url":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9"},
    {"name":"小陳滷社","address":"文化路","rating":"3.9","price":"$1-200","time":"11:30-20:00","url":"https://maps.app.goo.gl/1hxJG1hFFHHWA8c69"},
    {"name":"Café Wanderer","address":"陽明街","rating":"4.4","price":"$200-400","time":"10:00-20:30","url":"https://maps.app.goo.gl/fY6ryS1ZkMVXLkyC9"},
    {"name":"紅居館","address":"漢生西路","rating":"4.8","price":"$400-800","time":"17:00-23:30","url":"https://maps.app.goo.gl/pM2ksGeQ3Dw59zup6"},
    {"name":"津之芳","address":"漢生西路","rating":"4.2","price":"$200-400","time":"11:00-20:30","url":"https://maps.app.goo.gl/hXiBDGueUK27AxST8"},

    {"name":"海雲韓式","address":"自由路","rating":"4.7","price":"$400-600","time":"11:00-21:00","url":"https://maps.app.goo.gl/gQbAeUjs4MwnYePi7"},
    {"name":"NU PASTA","address":"陽明街","rating":"4.6","price":"$200-400","time":"11:00-21:00","url":"https://maps.app.goo.gl/DTTT1RdrE712kae49"},
    {"name":"麻丹辣","address":"漢生西路","rating":"4.9","price":"$200-400","time":"11:30-21:00","url":"https://maps.app.goo.gl/aM2oj5QoV2i7so3V7"},
    {"name":"山東寶","address":"幸福路","rating":"4.4","price":"$1-200","time":"11:30-21:00","url":"https://maps.app.goo.gl/ZKpyH4qKqAuFoKpy6"},
    {"name":"餵公子吃餅","address":"自由路","rating":"4.7","price":"$1-200","time":"14:00-18:00","url":"https://maps.app.goo.gl/6tcLqDACL4A8wtcbA"},

    {"name":"霸子牛排","address":"文化路","rating":"4.0","price":"$400-600","time":"11:00-21:30","url":"https://maps.app.goo.gl/4oLSG7m4w25Ehstm7"},
    {"name":"燒惑燒肉","address":"文化路","rating":"4.4","price":"$400-600","time":"12:00-22:30","url":"https://maps.app.goo.gl/aCYeMUYW4VZUrj7G7"},
    {"name":"食尚川府","address":"文化路","rating":"4.8","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/rhr1HHaZAV6XBR1z7"},
    {"name":"晨間廚房","address":"文化路","rating":"3.1","price":"$1-200","time":"07:00-14:30","url":"https://maps.app.goo.gl/o5Xa4dFAdgjGYqM28"},
    {"name":"龍一海南雞","address":"文化路","rating":"4.6","price":"$1-200","time":"10:30-19:00","url":"https://maps.app.goo.gl/H7s3eem2CT8p4JNJ8"},
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
        token = event["replyToken"]
        user_id = event["source"]["userId"]

        # =========================
        # 🎡 點轉盤 → 先問身份
        # =========================
        if msg == "美食轉盤":

            reply(token, [{
                "type": "template",
                "altText": "會員驗證",
                "template": {
                    "type": "buttons",
                    "text": "請問你是否為會員？",
                    "actions": [
                        {"type": "message","label":"我是會員","text":"我是會員"},
                        {"type": "message","label":"我不是會員","text":"我不是會員"}
                    ]
                }
            }])

        # =========================
        # ✅ 我是會員
        # =========================
        elif msg == "我是會員":

            reply(token, [
                {"type":"text","text":"🎡 轉盤開啟！"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        # =========================
        # ❌ 我不是會員
        # =========================
        elif msg == "我不是會員":

            reply(token, [
                {"type":"text","text":"👉 請先加入會員才能使用轉盤"},
                {"type":"text","text":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform"}
            ])

        # =========================
        # 🗺️ 美食地圖
        # =========================
        elif msg == "美食地圖":

            reply(token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"致理美食地圖",
                    "actions":[
                        {"type":"uri","label":"打開地圖","uri":"https://food-roulette-bot.onrender.com/map"}
                    ]
                }
            }])

        else:
            reply(token, [{"type":"text","text":"收到：" + msg}])

        return "OK"

    except:
        return "OK"


# =========================
# 🗺️ 地圖頁
# =========================
@app.route("/map")
def map_page():

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>致理美食地圖</title>

<style>
body{
    margin:0;
    font-family:Arial;
    display:flex;
    height:100vh;
}

#panel{
    width:420px;
    background:#fff8ee;
    padding:16px;
    overflow-y:auto;
}

.card{
    background:white;
    margin:12px 0;
    padding:14px;
    border-radius:16px;
    box-shadow:0 3px 10px rgba(0,0,0,0.08);
}

.name{
    font-size:17px;
    font-weight:800;
}

a{
    display:inline-block;
    margin-top:8px;
    background:#ff4d4d;
    color:white;
    padding:6px 10px;
    border-radius:8px;
    text-decoration:none;
}
</style>
</head>

<body>

<div id="panel">
<h2>🍜 致理美食清單</h2>
"""

    for p in places:
        html += f"""
        <div class="card">
            <div class="name">{p['name']}</div>
            ⭐ {p['rating']} | {p['price']}<br>
            🕒 {p['time']}<br>
            <a href="{p['url']}" target="_blank">📍 Google Maps</a>
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
