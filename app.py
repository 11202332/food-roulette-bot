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
# 📍 美食資料
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

    # 🎡 轉盤（不動）
    if msg == "美食轉盤":
        reply(reply_token, [
            {"type":"text","text":"🎡 轉盤功能"},
            {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
        ])

    # 🗺️ 地圖入口
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
# 🌍 地圖頁（精準校園版）
# =========================
@app.route("/map")
def map_page():

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>校園美食地圖</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>

<style>
body{
 margin:0;
 display:flex;
 height:100vh;
 font-family:Arial;
}

/* 🔥 地圖（主畫面加大） */
#map{
 flex: 1.5;
 height:100vh;
}

/* 右側卡片 */
#panel{
 width:360px;
 overflow-y:auto;
 background:#f8f8f8;
 padding:10px;
}

.card{
 background:white;
 margin:10px 0;
 padding:12px;
 border-radius:14px;
 box-shadow:0 2px 8px rgba(0,0,0,0.08);
 cursor:pointer;
 transition:0.2s;
}

.card:hover{
 transform:scale(1.02);
}

.card.active{
 border-left:5px solid #4CAF50;
 background:#f1fff4;
}

.title{
 font-size:17px;
 font-weight:700;
 display:flex;
 justify-content:space-between;
}

.tag{
 font-size:11px;
 padding:3px 8px;
 border-radius:999px;
}

.tag台式{background:#e3f2fd;color:#1565c0;}
.tag早午餐{background:#fff3e0;color:#ef6c00;}
.tag日式{background:#ede7f6;color:#5e35b1;}
.tag咖啡{background:#e8f5e9;color:#2e7d32;}

.meta{
 font-size:13px;
 color:#666;
 margin-top:6px;
}

.desc{
 font-size:13px;
 margin-top:4px;
 color:#444;
}
</style>
</head>

<body>

<div id="map"></div>
<div id="panel"></div>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<script>



// =========================
// 📍 地圖初始化（🔥精準鎖致理）
// =========================
var map = L.map('map', {
  center: [25.0218, 121.4636],   // ⭐ 往文化路巷弄偏移
  zoom: 18,                      // ⭐ 巷弄級別
  minZoom: 17,                   // ❌ 不讓縮到整個板橋
  maxZoom: 19,                   // ❌ 不讓放太遠
  zoomControl: true,
  scrollWheelZoom: true
});


// =========================
// 🔒 限制範圍（防亂拖）
// =========================
var bounds = L.latLngBounds(
  [25.0205, 121.4618],
  [25.0235, 121.4668]
);

map.setMaxBounds(bounds);
map.on('drag', function () {
  map.panInsideBounds(bounds, { animate: false });
});


// =========================
// 🌍 地圖底圖
// =========================
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
 attribution:''
}).addTo(map);


// =========================
// 📍 icon（穩定不飄）
// =========================
function getIcon(type){

 let color = "#2196F3";
 if(type==="台式") color="#f44336";
 if(type==="早午餐") color="#ff9800";
 if(type==="日式") color="#673ab7";
 if(type==="咖啡") color="#4caf50";

 return L.divIcon({
   className:"",
   html:`<div style="
      width:14px;height:14px;
      background:${color};
      border-radius:50%;
      border:2px solid white;
      box-shadow:0 0 6px rgba(0,0,0,0.3);
   "></div>`,
   iconSize:[14,14],
   iconAnchor:[7,7]
 });
}


// =========================
// 📍 資料
// =========================
var places = {{ places | tojson }};
var panel = document.getElementById("panel");
var markers = {};


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

 card.innerHTML = `
   <div class="title">
     ${p.name}
     <span class="tag tag${p.type}">${p.type}</span>
   </div>
   <div class="meta">
     ⭐ ${p.rating} ｜ 💰 ${p.price} ｜ 🕒 ${p.hours}
   </div>
   <div class="desc">${p.desc}</div>
 `;

 // 🔥 卡片 → 地圖連動
 card.onclick = () => {

   map.setView([p.lat, p.lng], 19, {animate:true});
   marker.openPopup();

   document.querySelectorAll(".card")
     .forEach(c=>c.classList.remove("active"));

   card.classList.add("active");

   card.scrollIntoView({behavior:"smooth", block:"center"});
 };

 panel.appendChild(card);
});

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
