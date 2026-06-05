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
# 🍜 店家資料（完整含 Google Maps）
# =========================
places = [
    {"name":"栄次郎個人燒肉—板橋文化店","rating":"4.7","price":"$200-400","comment":"燒肉很爽但錢包會痛","map":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
    {"name":"FlagPasta","rating":"4.5","price":"$200-400","comment":"穩定不踩雷","map":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
    {"name":"小食。候","rating":"4.3","price":"$200-400","comment":"安靜咖啡廳","map":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
    {"name":"義匠義式湯麵","rating":"4.8","price":"$200-400","comment":"湯麵很特別","map":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
    {"name":"鄉親小吃","rating":"4.6","price":"$1-200","comment":"便宜實在","map":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
    {"name":"台南無刺虱目魚","rating":"4.4","price":"$1-200","comment":"魚湯好喝","map":"https://maps.app.goo.gl/7b41uvR3Bimf2iGR8"},
    {"name":"逸麵鍋燒","rating":"4.9","price":"$1-200","comment":"湯頭超強","map":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
    {"name":"is pasta","rating":"4.3","price":"$200-400","comment":"學生聚餐","map":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"},
    {"name":"吉飽早餐","rating":"4.0","price":"$1-200","comment":"早八救星","map":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
    {"name":"太極鰲車輪餅","rating":"4.3","price":"$1-200","comment":"車輪餅讚","map":"https://maps.app.goo.gl/xYUnsWEWp4qL1Mg48"},
    {"name":"小松拉麵","rating":"4.5","price":"$1-200","comment":"平價拉麵","map":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"},
    {"name":"一京咖哩","rating":"4.6","price":"$1-200","comment":"咖哩濃","map":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8"},
    {"name":"致理飯糰","rating":"4.7","price":"$1-200","comment":"超大顆","map":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
    {"name":"吳二麻辣鴨血","rating":"4.4","price":"$1-200","comment":"冬天必吃","map":"https://maps.app.goo.gl/wTVnP3P1BeXfMweHA"},
    {"name":"吉野烤肉飯","rating":"3.8","price":"$1-200","comment":"快速便當","map":"https://maps.app.goo.gl/4NuMrst9S6LaLsAAA"},
    {"name":"MABO POKE","rating":"4.3","price":"$1-200","comment":"健康路線","map":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9"},
    {"name":"Café Wanderer","rating":"4.4","price":"$200-400","comment":"文青咖啡","map":"https://maps.app.goo.gl/fY6ryS1ZkMVXLkyC9"},
    {"name":"紅居館台菜","rating":"4.8","price":"$400-800","comment":"聚餐","map":"https://maps.app.goo.gl/pM2ksGeQ3Dw59zup6"},
    {"name":"海雲韓式料理","rating":"4.7","price":"$400-600","comment":"炸雞好吃","map":"https://maps.app.goo.gl/gQbAeUjs4MwnYePi7"},
    {"name":"NU PASTA","rating":"4.6","price":"$200-400","comment":"穩定","map":"https://maps.app.goo.gl/DTTT1RdrE712kae49"}
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

        # 🎡 轉盤（會員）
        if msg == "美食轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 會員功能"},
                {
                    "type":"template",
                    "altText":"會員選擇",
                    "template":{
                        "type":"buttons",
                        "text":"請選擇身份",
                        "actions":[
                            {"type":"message","label":"我是會員","text":"進入轉盤"},
                            {"type":"uri","label":"我不是會員",
                             "uri":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform?usp=header"}
                        ]
                    }
                }
            ])

        elif msg == "進入轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 轉盤開啟"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        # 🗺️ 地圖
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
# 🗺️ 地圖（完整可點 Google Maps）
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
    width:380px;
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
            {p['comment']}<br>

            <a href="{p['map']}" target="_blank">📍 開啟 Google Maps</a>
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
