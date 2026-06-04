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
# 📍 校園美食資料（50+ 可再擴充）
# =========================
places = [
    {"name":"致理飯糰","lat":25.0231,"lng":121.4675,"type":"台式","rating":4.3,"price":"$","hours":"06:30–10:30","desc":"學生早餐首選"},
    {"name":"小陳滷味","lat":25.0232,"lng":121.4676,"type":"台式","rating":4.5,"price":"$","hours":"17:00–23:30","desc":"宵夜排隊名店"},
    {"name":"油庫口麵線","lat":25.0238,"lng":121.4668,"type":"台式","rating":4.6,"price":"$","hours":"09:00–18:00","desc":"板橋必吃"},
    {"name":"麥當勞文化店","lat":25.0236,"lng":121.4679,"type":"早午餐","rating":4.2,"price":"$$","hours":"24H","desc":"讀書好去處"},
    {"name":"Sukiya","lat":25.0234,"lng":121.4676,"type":"日式","rating":4.4,"price":"$","hours":"24H","desc":"平價丼飯"},
    {"name":"路易莎","lat":25.0233,"lng":121.4673,"type":"咖啡","rating":4.4,"price":"$$","hours":"07:00–21:00","desc":"讀書咖啡廳"},
]

# =========================
# LINE webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    event = body["events"][0]

    if event["message"]["type"] != "text":
        return "OK"

    msg = event["message"]["text"]
    reply_token = event["replyToken"]

    if msg == "美食轉盤":
        reply(reply_token, [
            {"type":"text","text":"🎡 轉盤功能"},
            {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
        ])

    elif msg == "美食地圖":
        reply(reply_token, [{
            "type": "template",
            "altText": "美食地圖",
            "template": {
                "type": "buttons",
                "text": "🍜 致理美食地圖",
                "actions": [{
                    "type": "uri",
                    "label": "開啟地圖",
                    "uri": "https://food-roulette-bot.onrender.com/map"
                }]
            }
        }])

    else:
        reply(reply_token, [{"type":"text","text":"收到：" + msg}])

    return "OK"


# =========================
# 🌍 地圖頁（Leaflet 完整穩定版）
# =========================
@app.route("/map")
def map_page():

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>校園美食地圖</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>

<style>
body{
 margin:0;
 font-family:Arial;
 display:flex;
 height:100vh;
}

/* 左地圖 */
#map{
 flex:1;
 height:100vh;
}

/* 右卡片 */
#panel{
 width:380px;
 overflow:auto;
 background:#fafafa;
 padding:10px;
}

.card{
 background:white;
 margin:10px 0;
 padding:12px;
 border-radius:12px;
 box-shadow:0 2px 8px rgba(0,0,0,0.1);
 transition:0.2s;
 cursor:pointer;
}

.card.active{
 border-left:5px solid #4CAF50;
 background:#f0fff4;
}

.title{
 font-size:18px;
 font-weight:bold;
}

.tag{
 display:inline-block;
 padding:3px 8px;
 border-radius:999px;
 font-size:12px;
 margin-left:5px;
}

.tag台式{background:#e3f2fd;color:#1565c0;}
.tag早午餐{background:#fff3e0;color:#ef6c00;}
.tag日式{background:#ede7f6;color:#5e35b1;}
.tag咖啡{background:#f3e5ab;color:#6d4c41;}

.small{font-size:13px;color:#666}
</style>
</head>

<body>

<div id="map"></div>
<div id="panel"></div>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<script>
// =========================
// 📍 地圖初始化（修正：致理精準聚焦）
// =========================
var map = L.map('map').setView([25.0233, 121.4674], 18);

// OSM
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
 attribution:''
}).addTo(map);

// =========================
// 🔥 修正 Marker（不再飄移）
// =========================
function getIcon(type){
 let color = "blue";

 if(type==="台式") color="red";
 if(type==="早午餐") color="orange";
 if(type==="日式") color="purple";
 if(type==="咖啡") color="green";

 return L.divIcon({
   className:"custom-icon",
   html:`<div style="
      width:14px;height:14px;
      background:${color};
      border-radius:50%;
      border:2px solid white;
      box-shadow:0 0 6px rgba(0,0,0,0.3);
   "></div>`,
   iconSize:[14,14],
   iconAnchor:[7,7]   // ⭐ 關鍵：中心點鎖住
 });
}

// =========================
// 📍 資料
// =========================
var places = {{ places | tojson }};

var markers = {};

var panel = document.getElementById("panel");

// =========================
// 🧭 建立地圖 + 卡片
// =========================
places.forEach(p => {

 let marker = L.marker([p.lat, p.lng], {
   icon:getIcon(p.type)
 }).addTo(map)
 .bindPopup(`<b>${p.name}</b><br>${p.desc}`);

 markers[p.name] = marker;

 let card = document.createElement("div");
 card.className="card";
 card.id="card-"+p.name;

 card.innerHTML = `
   <div class="title">
     ${p.name}
     <span class="tag tag${p.type}">${p.type}</span>
   </div>
   <div class="small">⭐ ${p.rating} ｜ 💰 ${p.price}</div>
   <div class="small">${p.desc}</div>
   <div class="small">🕒 ${p.hours}</div>
 `;

 // =========================
 // 🔗 卡片點擊 → 地圖聯動
 // =========================
 card.onclick = () => {

   map.setView([p.lat, p.lng], 19, {
     animate:true
   });

   marker.openPopup();

   document.querySelectorAll(".card")
     .forEach(c=>c.classList.remove("active"));

   card.classList.add("active");

   card.scrollIntoView({behavior:"smooth", block:"center"});
 };

 panel.appendChild(card);
});

// =========================
// 🎯 初始聚焦（避免太廣）
// =========================
map.setView([25.0233, 121.4674], 18);
</script>

</body>
</html>
""", places=places)


# =========================
# home
# =========================
@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
