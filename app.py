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
    requests.post(
        LINE_API,
        headers=headers,
        data=json.dumps({"replyToken": reply_token, "messages": messages})
    )

# =========================
# 🍜 店家資料（不刪你的，做強化）
# =========================
places = [
{"name":"栄次郎燒肉","area":"文化","type":"燒肉","rating":4.7,"desc":"文化路燒肉","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
{"name":"FlagPasta","area":"陽明","type":"義大利麵","rating":4.5,"desc":"陽明街巷弄","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
{"name":"小食。候","area":"陽明","type":"咖啡","rating":4.3,"desc":"安靜咖啡廳","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
{"name":"義匠湯麵","area":"陽明","type":"麵食","rating":4.8,"desc":"陽明街主幹","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
{"name":"鄉親小吃","area":"幸福","type":"小吃","rating":4.6,"desc":"幸福路","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
{"name":"逸麵鍋燒","area":"新海","type":"火鍋","rating":4.9,"desc":"新海路","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
{"name":"is pasta","area":"文化","type":"義大利麵","rating":4.3,"desc":"文化路","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"},
{"name":"吉飽早餐","area":"文化","type":"早餐","rating":4.0,"desc":"文化路早餐","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
{"name":"致理飯糰","area":"文化","type":"早餐","rating":4.7,"desc":"學校旁","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
{"name":"小松拉麵","area":"陽明","type":"拉麵","rating":4.5,"desc":"自由路","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"},
{"name":"一京咖哩","area":"陽明","type":"咖哩","rating":4.6,"desc":"陽明街","url":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8"},
{"name":"MABO POKE","area":"文化","type":"健康","rating":4.3,"desc":"輕食","url":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9"},
{"name":"海雲韓式","area":"陽明","type":"韓式","rating":4.7,"desc":"韓式料理","url":"https://maps.app.goo.gl/gQbAeUjs4MwnYePi7"},
{"name":"紅居館","area":"新海","type":"台菜","rating":4.8,"desc":"聚餐","url":"https://maps.app.goo.gl/pM2ksGeQ3Dw59zup6"}
]


# =========================
# LINE webhook（✔轉盤完全不動）
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()

    try:
        event = body["events"][0]
        msg = event["message"]["text"]
        token = event["replyToken"]

        # 🎡 轉盤（完全保留你的）
        if msg == "美食轉盤":
            reply(token, [
                {"type":"text","text":"🎡 開啟轉盤"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        # 🗺️ 地圖
        elif msg == "美食地圖":
            reply(token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"致理美食手繪地圖",
                    "actions":[{
                        "type":"uri",
                        "label":"打開地圖",
                        "uri":"https://food-roulette-bot.onrender.com/map"
                    }]
                }
            }])

        else:
            reply(token,[{"type":"text","text":"收到：" + msg}])

        return "OK"

    except:
        return "OK"


# =========================
# 🗺️ 手繪地圖（重點修正版）
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
    display:flex;
    height:100vh;
    font-family:Arial;
    background:#f4efe6;
}

/* 左邊清單 */
#panel{
    width:350px;
    overflow:auto;
    padding:12px;
    background:#fff8ee;
}

.card{
    background:white;
    margin:8px 0;
    padding:10px;
    border-radius:12px;
    box-shadow:0 2px 6px rgba(0,0,0,0.08);
}

/* 右邊地圖 */
#map{
    flex:1;
    position:relative;
    background:#efe3cf;
}

/* 致理中心 */
.center{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    background:white;
    padding:8px 14px;
    border-radius:12px;
    font-weight:bold;
    color:#c0392b;
    box-shadow:0 2px 6px rgba(0,0,0,0.2);
}

/* 街道 */
.street{
    position:absolute;
    font-size:13px;
    font-weight:bold;
    color:#555;
}

.culture{top:8%;left:50%;}
.yangming{top:50%;right:6%;}
.xinhai{bottom:8%;left:50%;}
.happy{top:50%;left:6%;}

/* 點 */
.pin{
    position:absolute;
    transform:translate(-50%,-50%);
    text-align:center;
}

.dot{
    width:12px;height:12px;
    border-radius:50%;
    border:2px solid white;
    box-shadow:0 2px 6px rgba(0,0,0,0.2);
    margin:auto;
}

.label{
    font-size:10px;
    background:white;
    padding:2px 5px;
    border-radius:6px;
}

/* 顏色分類 */
.c1{background:#ff6b6b;}
.c2{background:#4dabf7;}
.c3{background:#51cf66;}
.c4{background:#f7b267;}
</style>

</head>

<body>

<div id="panel">
<h3>🍜 致理美食清單</h3>
"""

    # 左側（加完整資訊）
    for p in places:
        html += f"""
        <div class="card">
            <b>{p['name']}</b><br>
            ⭐ {p['rating']}<br>
            🍽 {p['type']}<br>
            📍 {p['desc']}<br>
            <a href="{p['url']}" target="_blank">Google Maps</a>
        </div>
        """

    html += """
</div>

<div id="map">

<div class="center">🎓 致理科技大學</div>

<div class="street culture">文化路</div>
<div class="street yangming">陽明街</div>
<div class="street xinhai">新海路</div>
<div class="street happy">幸福路</div>
"""

    # =========================
    # 📍 真正「不亂飄」版本
    # =========================
    for i, p in enumerate(places):

        # 顏色
        if p["type"] in ["燒肉","韓式","台菜"]:
            color="c1"
        elif p["type"] in ["咖啡","健康"]:
            color="c2"
        elif p["type"] in ["早餐","小吃"]:
            color="c3"
        else:
            color="c4"

        # 🎯 固定區域（不再亂跳）
        if p["area"] == "文化":
            top = 35 + (i % 4) * 6
            left = 50 + (i % 3 - 1) * 10

        elif p["area"] == "陽明":
            top = 50 + (i % 4) * 6
            left = 75 + (i % 3) * 6

        elif p["area"] == "新海":
            top = 75 + (i % 3) * 6
            left = 55 + (i % 3 - 1) * 8

        else:
            top = 55 + (i % 3) * 6
            left = 25 + (i % 3) * 8

        html += f"""
        <a href="{p['url']}" target="_blank">
        <div class="pin" style="top:{top}%;left:{left}%;">
            <div class="dot {color}"></div>
            <div class="label">{p['name']}</div>
        </div>
        </a>
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
