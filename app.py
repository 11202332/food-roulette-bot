from flask import Flask, request
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
# 📍 致理周邊（已修正：更集中文化路巷弄）
# =========================
CENTER_LAT = 25.0213
CENTER_LNG = 121.4625

places = [
    {"name":"致理飯糰","lat":25.0219,"lng":121.4632,"type":"台式","rating":4.3,"price":"$","hours":"06:30–10:30","desc":"學生早餐首選"},
    {"name":"小陳滷味","lat":25.0221,"lng":121.4635,"type":"台式","rating":4.5,"price":"$","hours":"17:00–23:30","desc":"宵夜排隊名店"},
    {"name":"油庫口麵線","lat":25.0210,"lng":121.4620,"type":"台式","rating":4.6,"price":"$","hours":"09:00–18:00","desc":"板橋經典必吃"},
    {"name":"麥當勞文化店","lat":25.0223,"lng":121.4640,"type":"早午餐","rating":4.2,"price":"$$","hours":"24小時","desc":"讀書好去處"},
    {"name":"Sukiya","lat":25.0208,"lng":121.4618,"type":"日式義式","rating":4.4,"price":"$","hours":"24小時","desc":"平價丼飯"},
    {"name":"路易莎","lat":25.0216,"lng":121.4628,"type":"咖啡","rating":4.4,"price":"$$","hours":"07:00–21:00","desc":"讀書咖啡廳"},
    {"name":"星巴克","lat":25.0217,"lng":121.4630,"type":"咖啡","rating":4.5,"price":"$$$","hours":"07:00–22:00","desc":"安靜空間"},
    {"name":"韓式小館","lat":25.0209,"lng":121.4622,"type":"異國","rating":4.2,"price":"$$","hours":"11:00–21:00","desc":"學生最愛韓式"},
]

# =========================
# LINE webhook（不動轉盤）
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()

    try:
        event = body["events"][0]

        if "message" not in event:
            return "OK"

        if event["message"]["type"] != "text":
            return "OK"

        reply_token = event["replyToken"]
        msg = event["message"]["text"]

        # 🎡 轉盤（完全保留不動）
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

        # 🗺️ 地圖入口（修正穩定版）
        elif msg == "美食地圖":

            reply(reply_token, [{
                "type": "template",
                "altText": "美食地圖",
                "template": {
                    "type": "buttons",
                    "text": "🍜 致理校園美食地圖（步行生活圈）",
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
        print(e)
        return "OK"


# =========================
# 🌍 MAP（修正：Zoom + Leaflet UX）
# =========================
@app.route("/map")
def map_page():

    google_key = os.environ.get("GOOGLE_MAPS_API_KEY", "")

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
    font-family: Arial;
    display:flex;
    height:100vh;
}}

/* 左地圖 */
#map {{
    flex: 1.2;
}}

/* 右卡片 */
#panel {{
    flex: 1;
    overflow-y: auto;
    background:#f7f7f7;
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
    font-size:16px;
    font-weight:700;
}}

.tag {{
    display:inline-block;
    padding:2px 8px;
    border-radius:999px;
    font-size:12px;
    margin-left:5px;
}}

.tag.blue {{background:#dbeafe; color:#1d4ed8;}}
.tag.orange {{background:#ffedd5; color:#c2410c;}}

.desc {{
    font-size:12px;
    color:#666;
}}

.price {{
    font-weight:bold;
    float:right;
}}
</style>

</head>

<body>

<div id="map"></div>
<div id="panel"></div>

<script>

// =========================
// 📍 地圖核心（修正：不再亂飛）
// =========================
const map = L.map('map', {{
    maxZoom: 19,
    minZoom: 16,
}}).setView([{CENTER_LAT}, {CENTER_LNG}], 18);

// OpenStreetMap
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: 'OSM'
}}).addTo(map);

// =========================
// 📍 Icon（修正：避免 marker 飄移）
// =========================
function getIcon(type) {{

    let color = "red";

    if(type==="咖啡") color="brown";
    if(type==="台式") color="red";
    if(type==="早午餐") color="green";
    if(type==="日式義式") color="blue";
    if(type==="異國") color="purple";

    return L.divIcon({{
        className: "custom-pin",
        html: `<div style="
            width:14px;
            height:14px;
            background:${{color}};
            border-radius:50%;
            border:2px solid white;
            box-shadow:0 2px 6px rgba(0,0,0,0.3);
            transform: translate(-50%, -50%);
        "></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7],   // 🔥 正確修正點：不再飄移
        popupAnchor: [0, -10]
    }});
}}

// =========================
// 📍 假資料
// =========================
const places = {json.dumps(places, ensure_ascii=False)};

let markers = [];

// =========================
// 📍 建 marker + card
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

    // card
    const panel = document.getElementById("panel");

    const tagColor = p.type==="咖啡" ? "blue" : "orange";

    panel.innerHTML += `
        <div class="card" id="card-${{i}}" onclick="focusMarker(${i})">
            <div class="title">
                ${{p.name}}
                <span class="tag ${{tagColor}}">${{p.type}}</span>
                <span class="price">${{p.price}}</span>
            </div>
            <div class="desc">${{p.desc}}</div>
            ⭐ ${{p.rating}} ｜ 🕒 ${{p.hours}}
        </div>
    `;
}});

// =========================
// 📍 卡片點擊 → 地圖連動
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
