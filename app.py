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

# =========================
# 模擬會員系統（先用假的，之後可串資料庫）
# =========================
def is_member(user_id):
    return True  # 你之後要做會員判斷再改這裡


def reply(reply_token, messages):
    payload = {
        "replyToken": reply_token,
        "messages": messages
    }
    requests.post(LINE_API, headers=headers, data=json.dumps(payload))


# =========================
# 🍜 店家資料（加強版）
# =========================
places = [
    {"name":"栄次郎個人燒肉","rating":"4.7","price":"$200-400","time":"11:30-23:30","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6","comment":"燒肉爽但錢包會痛，學生偶爾吃OK"},
    {"name":"FlagPasta","rating":"4.5","price":"$200-400","time":"11:00-21:00","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88","comment":"穩定不踩雷義大利麵"},
    {"name":"小食。候","rating":"4.3","price":"$200-400","time":"12:00-19:00","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66","comment":"文青小店，適合拍照"},
    {"name":"義匠義式湯麵","rating":"4.8","price":"$200-400","time":"11:30-21:00","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7","comment":"湯麵很穩，學生會回訪"},
    {"name":"鄉親小吃","rating":"4.6","price":"$1-200","time":"11:00-19:00","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8","comment":"便宜吃飽型，CP值高"},

    {"name":"台南虱目魚","rating":"4.4","price":"$1-200","time":"11:00-22:00","url":"https://maps.app.goo.gl/7b41uvR3Bimf2iGR8","comment":"便當救星，便宜又飽"},
    {"name":"逸麵麵鍋燒","rating":"4.9","price":"$1-200","time":"11:30-21:00","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8","comment":"超高分鍋燒麵"},
    {"name":"is pasta","rating":"4.3","price":"$200-400","time":"11:20-21:15","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7","comment":"學生聚餐常見"},
    {"name":"吉飽早餐","rating":"4.0","price":"$1-200","time":"7:00-14:00","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5","comment":"早八救命早餐店"},
    {"name":"太極鰲車輪餅","rating":"4.3","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/xYUnsWEWp4qL1Mg48","comment":"下午點心首選"},

    {"name":"小松拉麵","rating":"4.5","price":"$1-200","time":"11:30-21:30","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8","comment":"便宜拉麵能吃飽"},
    {"name":"一京咖哩","rating":"4.6","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8","comment":"咖哩穩定好吃"},
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
        user_id = event["source"]["userId"]

        # =========================
        # 🎡 點轉盤 → 先問身份
        # =========================
        if msg == "美食轉盤":

            reply(reply_token, [{
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

            if is_member(user_id):
                reply(reply_token, [
                    {"type":"text","text":"🎡 轉盤開啟！"},
                    {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
                ])
            else:
                reply(reply_token, [
                    {"type":"text","text":"⚠️ 你還不是會員喔"},
                    {"type":"text","text":"👉 請先填寫表單加入會員："},
                    {"type":"text","text":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform"}
                ])

        # =========================
        # ❌ 我不是會員
        # =========================
        elif msg == "我不是會員":

            reply(reply_token, [
                {"type":"text","text":"👉 請先加入會員才能使用轉盤"},
                {"type":"text","text":"表單如下："},
                {"type":"text","text":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform"}
            ])

        # =========================
        # 🗺️ 美食地圖
        # =========================
        elif msg == "美食地圖":

            reply(reply_token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"致理美食地圖",
                    "actions":[
                        {
                            "type":"uri",
                            "label":"打開地圖",
                            "uri":"https://food-roulette-bot.onrender.com/map"
                        }
                    ]
                }
            }])

        else:
            reply(reply_token, [{"type":"text","text":"收到：" + msg}])

        return "OK"

    except:
        return "OK"


# =========================
# 🗺️ 地圖頁（修正版）
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
    width:100%;
    max-width:520px;
    background:#fff8ee;
    padding:12px;
    overflow:auto;
}

.card{
    background:white;
    margin:10px 0;
    padding:12px;
    border-radius:14px;
    box-shadow:0 2px 6px rgba(0,0,0,0.1);
}

.name{
    font-size:16px;
    font-weight:bold;
}

.small{
    font-size:13px;
    color:#666;
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
            <div class="small">⭐ {p['rating']} | {p['price']} | {p['time']}</div>
            <div class="small">{p['comment']}</div>

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
