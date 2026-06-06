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
# 🍜 店家資料（已擴充 + 保留你原本）
# =========================
places = [
    {"name":"栄次郎個人燒肉","address":"文化路一段","rating":"4.7","price":"$200-400","time":"11:30-23:30","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6","comment":"肉好但荷包會痛，適合犒賞自己"},
    {"name":"FlagPasta","address":"陽明街","rating":"4.5","price":"$200-400","time":"11:00-21:00","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88","comment":"學生聚餐安全牌，不會踩雷"},
    {"name":"小食。候","address":"陽明街","rating":"4.3","price":"$200-400","time":"12:00-19:00","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66","comment":"氣氛舒服適合聊天"},
    {"name":"義匠義式湯麵","address":"陽明街","rating":"4.8","price":"$200-400","time":"11:30-21:00","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7","comment":"湯很香CP值高"},

    {"name":"鄉親小吃","address":"幸福路","rating":"4.6","price":"$1-200","time":"11:00-19:00","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8","comment":"古早味很有感"},
    {"name":"逸麵麵鍋燒","address":"新海路","rating":"4.9","price":"$1-200","time":"11:30-21:00","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGR8","comment":"料爆多直接吃飽"},
    {"name":"is pasta","address":"文化路","rating":"4.3","price":"$200-400","time":"11:20-21:15","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7","comment":"穩但要等位"},
    {"name":"吉飽早餐","address":"文化路","rating":"4.0","price":"$1-200","time":"7:00-14:00","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5","comment":"早八救命店"},
    {"name":"太極鰲車輪餅","address":"漢生西路","rating":"4.3","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/xYUnsWEWp4qL1Mg48","comment":"下午茶首選"},

    {"name":"小松拉麵","address":"自由路","rating":"4.5","price":"$1-200","time":"11:30-21:30","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8","comment":"便宜又能吃飽"},
    {"name":"一京咖哩","address":"陽明街","rating":"4.6","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8","comment":"咖哩很穩"},
    {"name":"致理飯糰","address":"文化路","rating":"4.7","price":"$1-200","time":"9:00-17:15","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5","comment":"學生早餐神器"},
    {"name":"吳二麻辣鴨血","address":"文化路","rating":"4.4","price":"$1-200","time":"10:30-20:30","url":"https://maps.app.goo.gl/wTVnP3P1BeXfMweHA","comment":"辣度很夠很爽"},
    {"name":"吉野烤肉飯","address":"文化路","rating":"3.8","price":"$1-200","time":"10:30-20:00","url":"https://maps.app.goo.gl/4NuMrst9S6LaLsAAA","comment":"便宜但普通"},

    {"name":"MABO POKE","address":"文化路","rating":"4.3","price":"$1-200","time":"11:00-20:30","url":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9","comment":"健康輕食"},
    {"name":"Café Wanderer","address":"陽明街","rating":"4.4","price":"$200-400","time":"10:00-20:30","url":"https://maps.app.goo.gl/fY6ryS1ZkMVXLkyC9","comment":"咖啡店很 chill"},
    {"name":"紅居館","address":"漢生西路","rating":"4.8","price":"$400-800","time":"17:00-23:30","url":"https://maps.app.goo.gl/pM2ksGeQ3Dw59zup6","comment":"聚餐很有面子"},
    {"name":"津之芳生魚片","address":"漢生西路","rating":"4.2","price":"$200-400","time":"11:00-20:30","url":"https://maps.app.goo.gl/hXiBDGueUK27AxST8","comment":"海鮮新鮮"},

    {"name":"海雲韓式料理","address":"自由路","rating":"4.7","price":"$400-600","time":"11:00-21:00","url":"https://maps.app.goo.gl/gQbAeUjs4MwnYePi7","comment":"韓式炸雞很強"},
    {"name":"韓鼓韓式料理","address":"新海路","rating":"4.3","price":"$400-600","time":"11:30-21:00","url":"https://maps.app.goo.gl/UmPfLfW57evBk1Yr8","comment":"小貴但好吃"},
    {"name":"川蜀麻辣食堂","address":"文化路","rating":"4.3","price":"$200-400","time":"11:00-22:00","url":"https://maps.app.goo.gl/c3XvA3uxBmn2fpys6","comment":"麻辣控會愛"},
]


# =========================
# LINE webhook（只修轉盤）
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()

    try:
        event = body["events"][0]
        msg = event["message"]["text"]
        reply_token = event["replyToken"]
        user_id = event["source"]["userId"]

        if msg == "美食地圖":
            reply(reply_token, [{
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

        # =========================
        # 🎡 修復：美食轉盤（你缺的就在這）
        # =========================
        elif msg == "美食轉盤":

            reply(reply_token, [{
                "type": "template",
                "altText": "會員驗證",
                "template": {
                    "type": "buttons",
                    "text": "請問你是否為會員？",
                    "actions": [
                        {
                            "type": "message",
                            "label": "我是會員",
                            "text": "我是會員"
                        },
                        {
                            "type": "message",
                            "label": "我不是會員",
                            "text": "我不是會員"
                        }
                    ]
                }
            }])

        elif msg == "我是會員":
            reply(reply_token, [
                {"type":"text","text":"🎡 轉盤開啟"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        elif msg == "我不是會員":
            reply(reply_token, [
                {"type":"text","text":"👉 請先加入會員"},
                {"type":"text","text":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform"}
            ])

        return "OK"

    except:
        return "OK"


# =========================
# 🗺️ 地圖 UI（不動）
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
    justify-content:center;
    background:linear-gradient(90deg,#ffe6d1,#fff,#ffe6d1);
}

#panel{
    width:650px;
    padding:25px;
    background:white;
    height:100vh;
    overflow:auto;
    box-shadow:0 0 25px rgba(0,0,0,0.15);
}

h2{
    text-align:center;
    font-size:26px;
}

.card{
    background:#fff7ef;
    margin:14px 0;
    padding:18px;
    border-radius:16px;
    font-size:16px;
}

.name{
    font-size:20px;
    font-weight:bold;
}

a{
    display:inline-block;
    margin-top:10px;
    background:#ff4d4d;
    color:white;
    padding:8px 12px;
    border-radius:10px;
    text-decoration:none;
    font-size:15px;
}
</style>
</head>

<body>

<div id="panel">
<h2>🍜 致理美食清單（加大版）</h2>
"""

    for p in places:
        html += f"""
        <div class="card">
            <div class="name">{p['name']}</div>
            ⭐ {p['rating']} | {p['price']}<br>
            📝 {p['comment']}<br>
            📍 {p['address']}<br>
            <a href="{p['url']}" target="_blank">Google Maps</a>
        </div>
        """

    html += """
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
