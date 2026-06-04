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
# 📍 校園美食資料（50+可擴充）
# =========================
places = [
    {"name":"致理飯糰","lat":25.0231,"lng":121.4675,"type":"台式","rating":4.3,"price":"$","hours":"06:30–10:30","desc":"學生早餐首選"},
    {"name":"小陳滷味","lat":25.0232,"lng":121.4676,"type":"台式","rating":4.5,"price":"$","hours":"17:00–23:30","desc":"宵夜排隊名店"},
    {"name":"阿房滷味","lat":25.0230,"lng":121.4672,"type":"台式","rating":4.2,"price":"$","hours":"16:30–23:00","desc":"經典滷味"},
    {"name":"油庫口麵線","lat":25.0238,"lng":121.4668,"type":"台式","rating":4.6,"price":"$","hours":"09:00–18:00","desc":"板橋必吃"},
    {"name":"麥當勞文化店","lat":25.0236,"lng":121.4679,"type":"早午餐","rating":4.2,"price":"$$","hours":"24小時","desc":"讀書好地方"},
    {"name":"麥味登","lat":25.0231,"lng":121.4671,"type":"早午餐","rating":4.0,"price":"$","hours":"06:00–13:30","desc":"早餐首選"},
    {"name":"晨間廚房","lat":25.0232,"lng":121.4672,"type":"早午餐","rating":4.1,"price":"$","hours":"06:00–14:00","desc":"學生早餐"},
    {"name":"Sukiya","lat":25.0234,"lng":121.4676,"type":"日式義式","rating":4.4,"price":"$","hours":"24小時","desc":"平價丼飯"},
    {"name":"薩莉亞","lat":25.0236,"lng":121.4678,"type":"日式義式","rating":4.1,"price":"$","hours":"11:00–22:00","desc":"義式平價"},
    {"name":"Is Pasta","lat":25.0233,"lng":121.4675,"type":"日式義式","rating":4.3,"price":"$$","hours":"11:00–21:30","desc":"義大利麵"},
    {"name":"路易莎","lat":25.0233,"lng":121.4673,"type":"咖啡","rating":4.4,"price":"$$","hours":"07:00–21:00","desc":"讀書咖啡"},
    {"name":"星巴克","lat":25.0236,"lng":121.4676,"type":"咖啡","rating":4.5,"price":"$$$","hours":"07:00–22:00","desc":"舒適環境"},
    {"name":"韓鼓韓式","lat":25.0230,"lng":121.4670,"type":"異國","rating":4.3,"price":"$$","hours":"11:00–21:00","desc":"韓式料理"},
    {"name":"泰品味","lat":25.0231,"lng":121.4671,"type":"異國","rating":4.2,"price":"$$","hours":"11:00–21:00","desc":"泰式料理"},
    {"name":"微笑炭烤","lat":25.0140,"lng":121.4620,"type":"宵夜","rating":4.3,"price":"$","hours":"18:00–01:00","desc":"宵夜烤肉"},
    {"name":"阿耀臭豆腐","lat":25.0141,"lng":121.4621,"type":"宵夜","rating":4.2,"price":"$","hours":"17:00–00:30","desc":"經典臭豆腐"},
]


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

        if event["message"]["type"] != "text":
            return "OK"

        reply_token = event["replyToken"]
        msg = event["message"]["text"]

        # 🎡 轉盤（完全保留）
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

        # 🗺️ 地圖入口（穩定版）
        elif msg == "美食地圖":

            reply(reply_token, [{
                "type": "template",
                "altText": "美食地圖",
                "template": {
                    "type": "buttons",
                    "text": "🍜 致理校園美食地圖",
                    "actions": [
                        {
                            "type": "uri",
                            "label": "打開探索地圖",
                            "uri": "https://food-roulette-bot.onrender.com/map"
                        }
                    ]
                }
            }])

        else:
            reply(reply_token, [
                {"type":"text","text":"收到：" + msg}
            ])

        return "OK"

    except:
        return "OK"


# =========================
# 🌍 Leaflet 地圖頁（穩定版 + 無API KEY）
# =========================
@app.route("/map")
def map_page():

    data_json = json.dumps(places, ensure_ascii=False)

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>校園美食地圖</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
body {{
    margin:0;
    display:flex;
    height:100vh;
    font-family:Arial;
}}

#map {{
    flex:1;
}}

#panel {{
    width:360px;
    overflow:auto;
    background:#f6f6f6;
    padding:10px;
}}

.card {{
    background:white;
    margin:10px;
    padding:12px;
    border-radius:14px;
    box-shadow:0 2px 6px rgba(0,0,0,0.1);
    cursor:pointer;
    transition:0.2s;
}}

.card:hover {{
    transform:scale(1.02);
}}

.card.active {{
    border:2px solid #4dabf7;
    background:#f1f9ff;
}}

.name {{
    font-size:18px;
    font-weight:bold;
}}

.tag {{
    display:inline-block;
    padding:3px 8px;
    border-radius:10px;
    font-size:12px;
    margin-right:6px;
    background:#eee;
}}

.price {{
    color:#ff6b6b;
    font-weight:bold;
}}

.marker {{
    width:14px;
    height:14px;
    border-radius:50%;
    border:2px solid white;
    box-shadow:0 0 6px rgba(0,0,0,0.3);
}}
</style>
</head>

<body>

<div id="map"></div>
<div id="panel"></div>

<script>

const places = {data_json};

const map = L.map('map').setView([25.02325, 121.46745], 18);

L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: 'OpenStreetMap'
}}).addTo(map);

let markerMap = {{}};
let cardMap = {{}};

function getColor(type) {{
    switch(type) {{
        case "台式": return "#ff6b6b";
        case "早午餐": return "#4dabf7";
        case "日式義式": return "#51cf66";
        case "咖啡": return "#fcc419";
        case "異國": return "#845ef7";
        case "宵夜": return "#ff922b";
        default: return "#adb5bd";
    }}
}}

function setActive(name) {{
    Object.values(cardMap).forEach(c => c.classList.remove("active"));
    if(cardMap[name]) {{
        cardMap[name].classList.add("active");
        cardMap[name].scrollIntoView({{behavior:"smooth", block:"center"}});
    }}
}}

function createMarker(p) {{
    const icon = L.divIcon({{
        className:"",
        html:`<div class="marker" style="background:${{getColor(p.type)}}"></div>`
    }});

    const marker = L.marker([p.lat, p.lng], {{icon}}).addTo(map)
        .bindPopup(`<b>${{p.name}}</b><br>${{p.desc}}`);

    marker.on("click", () => {{
        setActive(p.name);
    }});

    return marker;
}}

function render() {{
    const panel = document.getElementById("panel");
    panel.innerHTML = "";

    places.forEach(p => {{

        const marker = createMarker(p);
        markerMap[p.name] = marker;

        const card = document.createElement("div");
        card.className = "card";
        card.id = "card-" + p.name;

        card.innerHTML = `
            <div class="name">${{p.name}}</div>
            <div>
                <span class="tag">${{p.type}}</span>
                <span class="price">${{p.price}}</span>
            </div>
            <div style="font-size:12px;color:#666">${{p.desc}}</div>
            <div style="font-size:12px">⭐ ${{p.rating}} ｜ 🕒 ${{p.hours}}</div>
        `;

        card.onclick = () => {{
            map.setView([p.lat, p.lng], 19, {{animate:true}});
            marker.openPopup();
            setActive(p.name);
        }};

        panel.appendChild(card);
        cardMap[p.name] = card;
    }});
}}

render();

</script>
</body>
</html>
"""

    return html


# =========================
# home
# =========================
@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
