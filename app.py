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
    "Authorization": f"Bearer {LINE_TOKEN}" if LINE_TOKEN else ""
}


def reply(reply_token, messages):
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
# 🍜 你的完整店家資料（精簡放 name + url）
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
{"name":"小松拉麵","area":"陽明","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"},
{"name":"一京咖哩","area":"陽明","url":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8"},
{"name":"MABO POKE","area":"文化","url":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9"},
{"name":"海雲韓式","area":"陽明","url":"https://maps.app.goo.gl/gQbAeUjs4MwnYePi7"},
{"name":"紅居館","area":"新海","url":"https://maps.app.goo.gl/pM2ksGeQ3Dw59zup6"}
]


# =========================
# LINE webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    try:
        body = request.get_json()
        event = body["events"][0]
        msg = event["message"]["text"]
        reply_token = event["replyToken"]

        # 🎡 轉盤（會員功能）
        if msg == "美食轉盤":
            reply(reply_token, [{
                "type": "template",
                "altText": "會員功能",
                "template": {
                    "type": "buttons",
                    "text": "🎡 此為會員功能",
                    "actions": [
                        {
                            "type": "uri",
                            "label": "會員登入",
                            "uri": "https://cute-melomakarona-859d27.netlify.app"
                        },
                        {
                            "type": "uri",
                            "label": "非會員填寫",
                            "uri": "https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform?usp=header"
                        }
                    ]
                }
            }])

        # 🗺️ 地圖
        elif msg == "美食地圖":
            reply(reply_token, [{
                "type": "text",
                "text": "🗺️ 地圖：https://food-roulette-bot.onrender.com/map"
            }])

        else:
            reply(reply_token, [{"type":"text","text":"收到：" + msg}])

        return "OK"

    except Exception as e:
        print(e)
        return "OK"


# =========================
# 🗺️ 地圖（真正不擠版本）
# =========================
@app.route("/map")
def map_page():

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>致理美食地圖</title>

<style>
body{
    margin:0;
    font-family:Arial;
    background:#f7f3ea;
}

.container{
    display:flex;
    height:100vh;
}

#panel{
    width:320px;
    background:#fff8ee;
    padding:10px;
    overflow:auto;
}

.card{
    background:white;
    margin:8px 0;
    padding:10px;
    border-radius:12px;
}

#map{
    flex:1;
    position:relative;
    background:#f1eadf;
}

.center{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    background:white;
    padding:6px 12px;
    border-radius:10px;
    font-weight:bold;
}

.food{
    position:absolute;
    transform:translate(-50%,-50%);
    text-align:center;
}

.pin{
    width:12px;height:12px;
    border-radius:50%;
    border:2px solid white;
    margin:auto;
}

.label{
    font-size:10px;
    background:white;
    padding:2px 5px;
    border-radius:8px;
}

/* 📱 手機 */
@media (max-width:768px){
    .container{flex-direction:column;}
    #panel{width:100%;height:40vh;}
    #map{height:60vh;}
}
</style>

</head>

<body>

<div class="container">

<div id="panel">
<h3>🍜 致理美食</h3>
"""

    for p in places:
        html += f"""
        <div class="card">
            <b>{p['name']}</b><br>
            <a href="{p['url']}" target="_blank">📍 Google Maps</a>
        </div>
        """

    html += """
</div>

<div id="map">
<div class="center">🎓 致理科技大學</div>
"""

    # 🎯 真正分散（依 index + jitter）
    for i, p in enumerate(places):

        base_x = (i % 6) * 14 + 10
        base_y = (i // 6) * 14 + 10

        jitter_x = (i * 3) % 7
        jitter_y = (i * 5) % 7

        top = min(88, base_y + jitter_y)
        left = min(88, base_x + jitter_x)

        html += f"""
        <div class="food" style="top:{top}%;left:{left}%;">
            <div class="pin"></div>
            <div class="label">{p['name']}</div>
        </div>
        """

    html += """
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
