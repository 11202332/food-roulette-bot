from flask import Flask, request, render_template_string
import requests
import os
import json
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
LINE_API = "https://api.line.me/v2/bot/message/reply"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_TOKEN}"
}


# =========================
# LINE reply function
# =========================
def reply(reply_token, messages):
    payload = {
        "replyToken": reply_token,
        "messages": messages
    }
    requests.post(LINE_API, headers=headers, data=json.dumps(payload))


# =========================
# 📍 致理中心點
# =========================
CENTER = (25.0240, 121.4705)


# =========================
# 🍜 店家資料（已加基本座標）
# =========================
places = [
{
"name":"栄次郎個人燒肉",
"lat":25.02396,
"lng":121.47162,
"rating":4.7,
"price":"$200-400",
"url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"
},
{
"name":"FlagPasta",
"lat":25.02410,
"lng":121.46985,
"rating":4.5,
"price":"$200-400",
"url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"
},
{
"name":"小食。候",
"lat":25.02430,
"lng":121.46970,
"rating":4.3,
"price":"$200-400",
"url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"
},
{
"name":"義匠義式湯麵",
"lat":25.02420,
"lng":121.47080,
"rating":4.8,
"price":"$200-400",
"url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"
},
{
"name":"鄉親小吃",
"lat":25.02350,
"lng":121.46990,
"rating":4.6,
"price":"$1-200",
"url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"
},
{
"name":"逸麵鍋燒",
"lat":25.02280,
"lng":121.47100,
"rating":4.9,
"price":"$1-200",
"url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"
},
{
"name":"is pasta",
"lat":25.02450,
"lng":121.47120,
"rating":4.3,
"price":"$200-400",
"url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"
},
{
"name":"吉飽早餐",
"lat":25.02460,
"lng":121.47060,
"rating":4.0,
"price":"$1-200",
"url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"
},
{
"name":"致理飯糰",
"lat":25.02470,
"lng":121.47040,
"rating":4.7,
"price":"$1-200",
"url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"
},
{
"name":"小松拉麵",
"lat":25.02520,
"lng":121.47110,
"rating":4.5,
"price":"$1-200",
"url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"
}
]


# =========================
# 🧭 距離計算
# =========================
def distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c


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

        # 🎡 轉盤
        if msg == "美食轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 開啟轉盤"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        # 🗺️ 地圖
        elif msg == "美食地圖":
            reply(reply_token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"致理互動美食地圖",
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
# 🗺️ Leaflet 真實地圖
# =========================
@app.route("/map")
def map_page():

    # 🔥 距離排序（致理最近）
    sorted_places = sorted(
        places,
        key=lambda p: distance(CENTER[0], CENTER[1], p["lat"], p["lng"])
    )

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>致理美食地圖</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
body { margin:0; font-family:Arial; }
#map { height:100vh; width:100vw; }
.panel {
    position:absolute;
    top:10px;
    left:10px;
    background:white;
    padding:10px;
    z-index:999;
    border-radius:10px;
    max-height:90vh;
    overflow:auto;
}
.item {
    font-size:13px;
    margin:5px 0;
    cursor:pointer;
}
</style>
</head>

<body>

<div id="map"></div>

<div class="panel">
<b>🍜 致理美食（最近排序）</b><br><br>
"""

    for p in sorted_places:
        html += f"""
<div class="item" onclick="go({p['lat']},{p['lng']})">
{p['name']} ({p['rating']})
</div>
"""

    html += """
</div>

<script>

// 🗺️ 地圖
var map = L.map('map').setView([25.0240, 121.4705], 16);

// 🗺️ OpenStreetMap底圖
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

// 🎓 致理
L.marker([25.0240, 121.4705]).addTo(map)
.bindPopup("🎓 致理科技大學");

// 🍜 店家
"""

    for p in places:
        html += f"""
L.marker([{p['lat']},{p['lng']}]).addTo(map)
.bindPopup(`
<b>{p['name']}</b><br>
⭐ {p['rating']}<br>
<a href="{p['url']}" target="_blank">Google Maps</a>
`);
"""

    html += """

function go(lat,lng){
    map.setView([lat,lng],18);
}

</script>

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
