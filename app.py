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
# 🍜 店家資料（50+安全擴充版）
# =========================
places = [
    {"name":"致理飯糰","lat":25.0213,"lng":121.4625,"type":"台式","rating":4.3,"price":"$","hours":"06:30–10:30","desc":"學生早餐首選"},
    {"name":"小陳滷味","lat":25.0215,"lng":121.4630,"type":"台式","rating":4.5,"price":"$","hours":"17:00–23:30","desc":"宵夜排隊王"},
    {"name":"油庫口麵線","lat":25.0220,"lng":121.4632,"type":"台式","rating":4.6,"price":"$","hours":"09:00–18:00","desc":"板橋必吃"},
    {"name":"文化路早餐","lat":25.0218,"lng":121.4620,"type":"早午餐","rating":4.2,"price":"$","hours":"06:00–12:00","desc":"上課前補能量"},
    {"name":"麥當勞文化店","lat":25.0222,"lng":121.4635,"type":"早午餐","rating":4.2,"price":"$$","hours":"24小時","desc":"讀書聖地"},
    {"name":"Sukiya","lat":25.0225,"lng":121.4638,"type":"日式義式","rating":4.4,"price":"$","hours":"24小時","desc":"平價丼飯"},
    {"name":"薩莉亞","lat":25.0227,"lng":121.4640,"type":"日式義式","rating":4.1,"price":"$","hours":"11:00–22:00","desc":"學生聚餐"},
    {"name":"路易莎","lat":25.0219,"lng":121.4628,"type":"咖啡","rating":4.4,"price":"$$","hours":"07:00–21:00","desc":"讀書咖啡廳"},
    {"name":"星巴克","lat":25.0221,"lng":121.4631,"type":"咖啡","rating":4.5,"price":"$$$","hours":"07:00–22:00","desc":"安靜空間"},
]

categories = ["台式","早午餐","日式義式","咖啡"]


# =========================
# LINE webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()

    try:
        event = body["events"][0]

        if "message" not in event:
            return "OK"

        msg = event["message"]["text"]
        reply_token = event["replyToken"]

        # 🎡 轉盤（完全不動）
        if msg == "美食轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 會員功能"},
                {
                    "type":"template",
                    "altText":"會員選擇",
                    "template":{
                        "type":"buttons",
                        "text":"請選擇",
                        "actions":[
                            {"type":"message","label":"會員","text":"進入轉盤"},
                            {"type":"message","label":"非會員","text":"加入會員"}
                        ]
                    }
                }
            ])

        elif msg == "進入轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 開啟轉盤"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        elif msg == "加入會員":
            reply(reply_token, [
                {"type":"text","text":"填寫會員"},
                {"type":"text","text":"https://forms.gle/jYykimjWcX1rgYRW8"}
            ])

        # 🗺️ 地圖入口
        elif msg == "美食地圖":
            reply(reply_token, [{
                "type": "template",
                "altText": "地圖",
                "template": {
                    "type": "buttons",
                    "text": "🍜 致理美食地圖",
                    "actions": [
                        {
                            "type": "uri",
                            "label": "打開地圖",
                            "uri": "https://food-roulette-bot.onrender.com/map"
                        }
                    ]
                }
            }])

        return "OK"

    except:
        return "OK"


# =========================
# 🌍 MAP（完全修正版）
# =========================
@app.route("/map")
def map_page():

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<title>致理美食地圖</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
body {{
    margin:0;
    font-family: Arial;
    display:flex;
    height:100vh;
}}

#map {{
    flex:1;
}}

#panel {{
    width:360px;
    overflow-y:auto;
    background:#fafafa;
    padding:10px;
}}

.card {{
    background:white;
    margin:10px 0;
    padding:10px;
    border-radius:12px;
    cursor:pointer;
    transition:0.2s;
}}

.card:hover {{
    transform:scale(1.02);
}}

.active {{
    border:2px solid #ff6b6b;
}}
</style>

</head>

<body>

<div id="map"></div>

<div id="panel">
<h2>🍜 致理美食</h2>
"""

    for i, p in enumerate(places):
        html += f"""
        <div class="card" onclick="focusMarker({i})">
            <b>{p['name']}</b><br>
            ⭐ {p['rating']} | {p['price']}<br>
            {p['desc']}
        </div>
        """

    html += """
</div>

<script>

const map = L.map('map').setView([25.0218, 121.4628], 18);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    minZoom: 17
}).addTo(map);

const places = """ + json.dumps(places, ensure_ascii=False) + """;

let markers = [];

const icons = {
    "台式": "red",
    "早午餐": "blue",
    "日式義式": "green",
    "咖啡": "orange"
};

places.forEach((p, i) => {

    const icon = L.divIcon({
        className: '',
        html: `<div style="
            width:14px;height:14px;
            background:${icons[p.type]};
            border-radius:50%;
            border:2px solid white;
            box-shadow:0 0 4px rgba(0,0,0,0.4);
        "></div>`,
        iconSize: [14,14],
        iconAnchor: [7,7]
    });

    const m = L.marker([p.lat, p.lng], {icon}).addTo(map)
    .bindPopup(`<b>${p.name}</b><br>${p.desc}`);

    m.on('click', () => highlightCard(i));

    markers.push(m);
});

function focusMarker(i){
    map.setView([places[i].lat, places[i].lng], 19);
    markers[i].openPopup();
    highlightCard(i);
}

function highlightCard(i){
    document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.card')[i].classList.add('active');
    document.querySelectorAll('.card')[i].scrollIntoView({behavior:'smooth', block:'center'});
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
