from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# =========================
# LINE API
# =========================
LINE_TOKEN = os.environ.get("LINE_TOKEN")
LINE_API = "https://api.line.me/v2/bot/message/reply"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_TOKEN}" if LINE_TOKEN else ""
}

def reply(reply_token, messages):
    """安全版 reply（避免 LINE_TOKEN 沒設炸掉）"""
    if not LINE_TOKEN:
        print("⚠️ LINE_TOKEN 未設定")
        return

    payload = {
        "replyToken": reply_token,
        "messages": messages
    }

    try:
        requests.post(LINE_API, headers=headers, data=json.dumps(payload))
    except Exception as e:
        print("Reply error:", e)


# =========================
# 📍 致理中心點（固定）
# =========================
CENTER_LAT = 25.0213
CENTER_LNG = 121.4625


# =========================
# 🍜 店家資料（穩定精簡版 8~50家都可擴充）
# =========================
places = [
    {"name":"致理飯糰","lat":25.0219,"lng":121.4632,"type":"台式","rating":4.3,"price":"$","hours":"06:30–10:30","desc":"學生早餐首選"},
    {"name":"小陳滷味","lat":25.0221,"lng":121.4635,"type":"台式","rating":4.5,"price":"$","hours":"17:00–23:30","desc":"宵夜排隊名店"},
    {"name":"油庫口麵線","lat":25.0210,"lng":121.4620,"type":"台式","rating":4.6,"price":"$","hours":"09:00–18:00","desc":"板橋必吃"},
    {"name":"麥當勞文化店","lat":25.0223,"lng":121.4640,"type":"早午餐","rating":4.2,"price":"$$","hours":"24小時","desc":"讀書好地方"},
    {"name":"Sukiya","lat":25.0208,"lng":121.4618,"type":"日式義式","rating":4.4,"price":"$","hours":"24小時","desc":"平價丼飯"},
    {"name":"路易莎","lat":25.0216,"lng":121.4628,"type":"咖啡","rating":4.4,"price":"$$","hours":"07:00–21:00","desc":"讀書咖啡廳"},
    {"name":"星巴克","lat":25.0217,"lng":121.4630,"type":"咖啡","rating":4.5,"price":"$$$","hours":"07:00–22:00","desc":"安靜空間"},
    {"name":"韓式小館","lat":25.0209,"lng":121.4622,"type":"異國","rating":4.2,"price":"$$","hours":"11:00–21:00","desc":"學生最愛"}
]


# =========================
# LINE Webhook（完全防炸版）
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    try:
        body = request.get_json()

        if not body or "events" not in body:
            return "OK"

        if len(body["events"]) == 0:
            return "OK"

        event = body["events"][0]

        if "message" not in event:
            return "OK"

        if event["message"]["type"] != "text":
            return "OK"

        reply_token = event.get("replyToken")
        msg = event["message"]["text"]

        if not reply_token:
            return "OK"


        # =========================
        # 🎡 轉盤（完全保留）
        # =========================
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
                {"type":"text","text":"🎡 開啟美食轉盤👇"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])


        elif msg == "加入會員":

            reply(reply_token, [
                {"type":"text","text":"📝 請填寫會員表單"},
                {"type":"text","text":"https://forms.gle/jYykimjWcX1rgYRW8"}
            ])


        # =========================
        # 🗺️ 地圖入口
        # =========================
        elif msg == "美食地圖":

            reply(reply_token, [{
                "type": "template",
                "altText": "美食地圖",
                "template": {
                    "type": "buttons",
                    "text": "🍜 致理周邊美食地圖",
                    "actions": [
                        {
                            "type": "uri",
                            "label": "打開地圖",
                            "uri": "https://food-roulette-bot.onrender.com/map"
                        }
                    ]
                }
            }])


        else:
            reply(reply_token, [{"type":"text","text":"收到：" + msg}])


        return "OK"

    except Exception as e:
        print("WEBHOOK ERROR:", e)
        return "OK"


# =========================
# 🌍 MAP（Leaflet + 不飄移 + 聚焦致理）
# =========================
@app.route("/map")
def map_page():

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>致理美食地圖</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<style>
body {{
    margin:0;
    display:flex;
    height:100vh;
    font-family: Arial;
}}

/* 左地圖 */
#map {{
    flex: 1.3;
}}

/* 右卡片 */
#panel {{
    flex: 1;
    overflow-y:auto;
    background:#f5f5f5;
    padding:10px;
}}

.card {{
    background:white;
    margin:10px;
    padding:12px;
    border-radius:14px;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
    cursor:pointer;
}}

.card:hover {{
    transform:scale(1.01);
}}

.title {{
    font-weight:700;
}}

.tag {{
    font-size:12px;
    padding:2px 8px;
    border-radius:999px;
    margin-left:6px;
}}

.blue {{background:#dbeafe; color:#1d4ed8;}}
.orange {{background:#ffedd5; color:#c2410c;}}
.green {{background:#dcfce7; color:#166534;}}
.brown {{background:#fef3c7; color:#92400e;}}
</style>
</head>

<body>

<div id="map"></div>
<div id="panel"></div>

<script>

// =========================
// 📍 地圖（鎖定致理）
// =========================
const map = L.map('map', {{
    minZoom: 16,
    maxZoom: 19
}}).setView([{CENTER_LAT}, {CENTER_LNG}], 18);

// OSM
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: 'OSM'
}}).addTo(map);


// =========================
// 📍 icon（完全修正飄移）
// =========================
function getIcon(type) {{

    let color = "red";
    if(type==="咖啡") color="brown";
    if(type==="台式") color="red";
    if(type==="早午餐") color="green";
    if(type==="日式義式") color="blue";
    if(type==="異國") color="purple";

    return L.divIcon({{
        className: "",
        html: `<div style="
            width:14px;
            height:14px;
            background:${{color}};
            border-radius:50%;
            border:2px solid white;
            transform: translate(-50%, -50%);
            box-shadow:0 2px 6px rgba(0,0,0,0.3);
        "></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7],
        popupAnchor: [0, -10]
    }});
}}

// =========================
// 📍 data
// =========================
const places = {{json.dumps(places, ensure_ascii=False)}};

let markers = [];

// =========================
// 📍 build UI
// =========================
places.forEach((p, i) => {{

    const marker = L.marker([p.lat, p.lng], {{
        icon: getIcon(p.type)
    }}).addTo(map)
    .bindPopup(`<b>${{p.name}}</b><br>${{p.desc}}`);

    markers.push(marker);

    marker.on("click", () => {{
        map.setView([p.lat, p.lng], 19);
        document.getElementById("card-"+i).scrollIntoView({{behavior:"smooth"}});
    }});

    const panel = document.getElementById("panel");

    let tagClass = "orange";
    if(p.type==="咖啡") tagClass="brown";
    if(p.type==="早午餐") tagClass="green";

    panel.innerHTML += `
        <div class="card" id="card-${{i}}" onclick="focusMarker(${i})">
            <div class="title">
                ${{p.name}}
                <span class="tag ${{tagClass}}">${{p.type}}</span>
            </div>
            <div style="font-size:12px;color:#666">${{p.desc}}</div>
            ⭐ ${{p.rating}} ｜ 🕒 ${{p.hours}} ｜ $${{p.price}}
        </div>
    `;
}});

// =========================
// 📍 card → map
// =========================
function focusMarker(i){{
    const m = markers[i];
    map.setView(m.getLatLng(), 19);
    m.openPopup();
}}

</script>

</body>
</html>
"""

    return html


@app.route("/")
def home():
    return "Bot Running"


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
