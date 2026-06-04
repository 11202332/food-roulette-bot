from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# =========================
# LINE BOT
# =========================
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
# Google Maps Key（可為空）
# =========================
GOOGLE_MAPS_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")


# =========================
# 店家資料
# =========================
places = [
    {"name":"致理飯糰","lat":25.0231,"lng":121.4675,"type":"台式","rating":4.3,"price":"$","hours":"06:30–10:30","desc":"學生早餐首選"},
    {"name":"小陳滷味","lat":25.0232,"lng":121.4676,"type":"台式","rating":4.5,"price":"$","hours":"17:00–23:30","desc":"宵夜排隊名店"},
    {"name":"油庫口麵線","lat":25.0238,"lng":121.4668,"type":"台式","rating":4.6,"price":"$","hours":"09:00–18:00","desc":"板橋經典必吃"},
    {"name":"麥當勞文化店","lat":25.0236,"lng":121.4679,"type":"早午餐","rating":4.2,"price":"$$","hours":"24小時","desc":"讀書好去處"},
    {"name":"Sukiya","lat":25.0234,"lng":121.4676,"type":"日式義式","rating":4.4,"price":"$","hours":"24小時","desc":"平價丼飯"},
    {"name":"路易莎","lat":25.0233,"lng":121.4673,"type":"咖啡","rating":4.4,"price":"$$","hours":"07:00–21:00","desc":"讀書咖啡廳"},
]

categories = ["台式","早午餐","日式義式","咖啡"]


# =========================
# LINE Webhook（轉盤完全不動）
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

        # 🎡 轉盤
        if msg == "美食轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 此功能為會員功能"},
                {
                    "type":"template",
                    "altText":"會員選擇",
                    "template":{
                        "type":"buttons",
                        "text":"請選擇身份",
                        "actions":[
                            {"type":"message","label":"我是會員","text":"進入轉盤"},
                            {"type":"message","label":"我不是會員","text":"加入會員"}
                        ]
                    }
                }
            ])

        elif msg == "進入轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 開啟美食轉盤"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        elif msg == "加入會員":
            reply(reply_token, [
                {"type":"text","text":"📝 會員表單"},
                {"type":"text","text":"https://forms.gle/jYykimjWcX1rgYRW8"}
            ])

        elif msg == "美食地圖":
            reply(reply_token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"🍜 校園美食地圖",
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
# 🌍 地圖頁（安全版：沒 Key 也能開）
# =========================
@app.route("/map")
def map_page():

    places_json = json.dumps(places, ensure_ascii=False)

    # 👉 沒 key 直接顯示「提示版 UI」
    if not GOOGLE_MAPS_KEY:
        html = f"""
        <html>
        <meta charset="utf-8">
        <body style="font-family:Arial;background:#f5f5f5;text-align:center;padding:50px">

            <h2>⚠️ Google Maps 尚未設定</h2>
            <p>你目前還沒有設定 GOOGLE_MAPS_API_KEY</p>

            <div style="margin-top:20px;background:white;padding:20px;border-radius:12px;display:inline-block">
                <p>👉 Render → Environment Variables</p>
                <p>新增：</p>
                <code>GOOGLE_MAPS_API_KEY = 你的key</code>
            </div>

            <h3 style="margin-top:30px">📍 仍可查看資料（測試模式）</h3>

            {places_json}

        </body>
        </html>
        """
        return html


    # =========================
    # 有 Key 才跑 Google Maps UI
    # =========================
    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>校園美食地圖</title>

<style>
body {{
    margin:0;
    font-family:Arial;
}}

.container {{
    display:flex;
    height:100vh;
}}

#map {{
    flex:1;
}}

.panel {{
    width:420px;
    overflow-y:auto;
    background:#f7f7f7;
    padding:10px;
}}

.card {{
    background:white;
    margin:10px 0;
    padding:12px;
    border-radius:14px;
    box-shadow:0 2px 8px rgba(0,0,0,0.1);
    cursor:pointer;
}}

.title {{
    font-size:18px;
    font-weight:800;
}}

.badge {{
    display:inline-block;
    padding:3px 8px;
    border-radius:20px;
    font-size:12px;
    margin-right:5px;
}}

.price {{
    background:#ffeaa7;
}}

.type {{
    background:#81ecec;
}}

.desc {{
    font-size:13px;
    color:#444;
    margin-top:4px;
}}

</style>
</head>

<body>

<div class="container">
    <div id="map"></div>
    <div class="panel" id="panel"></div>
</div>

<script>
let map;
let markers = [];
let infoWindow;

const places = {places_json};

function initMap() {{

    map = new google.maps.Map(document.getElementById("map"), {{
        center: {{ lat: 25.0231, lng: 121.4675 }},
        zoom: 16
    }});

    infoWindow = new google.maps.InfoWindow();

    const panel = document.getElementById("panel");

    places.forEach((p, i) => {{

        const marker = new google.maps.Marker({{
            position: {{ lat: p.lat, lng: p.lng }},
            map,
            title: p.name
        }});

        markers.push(marker);

        marker.addListener("click", () => openInfo(i));

        const card = document.createElement("div");
        card.className = "card";

        card.innerHTML = `
            <div class="title">🍜 ${{p.name}}</div>
            <div>
                <span class="badge type">${{p.type}}</span>
                <span class="badge price">${{p.price}}</span>
            </div>
            <div class="desc">${{p.desc}}</div>
            <div style="font-size:13px;">⭐ ${{p.rating}} ｜ 🕒 ${{p.hours}}</div>
        `;

        card.onclick = () => openInfo(i);
        panel.appendChild(card);

    }});
}}

function openInfo(i) {{
    const p = places[i];

    map.panTo({{ lat: p.lat, lng: p.lng }});
    map.setZoom(18);

    infoWindow.setContent(`
        <b>${{p.name}}</b><br>
        ⭐ ${{p.rating}}<br>
        🕒 ${{p.hours}}
    `);

    infoWindow.open(map, markers[i]);
}}
</script>

<script
src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_KEY or ''}&callback=initMap"
async defer>
</script>

</body>
</html>
"""

    return html


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
