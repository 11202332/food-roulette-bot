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
# 🍜 店家資料
# =========================

base_lat = 25.0250
base_lng = 121.4630

def gen_coord(i):
    return base_lat + (i * 0.00015), base_lng + (i * 0.00012)

raw_places = [
{"name":"栄次郎個人燒肉","rating":4.7,"price":"$200-400","type":"燒肉","comment":"自己烤肉很爽但錢包會痛"},
{"name":"FlagPasta","rating":4.5,"price":"$200-400","type":"義大利麵","comment":"穩定不踩雷"},
{"name":"小食。候","rating":4.3,"price":"$200-400","type":"咖啡","comment":"安靜但容易客滿"},
{"name":"義匠義式湯麵","rating":4.8,"price":"$200-400","type":"義大利麵","comment":"濃郁湯麵很特別"},
{"name":"鄉親小吃","rating":4.6,"price":"$1-200","type":"小吃","comment":"便宜實在"},
{"name":"台南無刺虱目魚","rating":4.4,"price":"$1-200","type":"小吃","comment":"清爽魚湯"},
{"name":"逸麵鍋燒","rating":4.9,"price":"$1-200","type":"鍋燒","comment":"湯頭超強"},
{"name":"is pasta","rating":4.3,"price":"$200-400","type":"義大利麵","comment":"學生聚餐常去"},
{"name":"吉飽早餐","rating":4.0,"price":"$1-200","type":"早餐","comment":"早八救星"},
{"name":"致理飯糰","rating":4.7,"price":"$1-200","type":"早餐","comment":"飯糰超大顆"},
{"name":"吳二麻辣鴨血","rating":4.4,"price":"$1-200","type":"麻辣","comment":"冬天必吃"},
{"name":"吉野烤肉飯","rating":3.8,"price":"$1-200","type":"便當","comment":"快速解決"},
{"name":"MABO POKE","rating":4.3,"price":"$1-200","type":"健康","comment":"清爽路線"},
]

places = []
for i, p in enumerate(raw_places):
    lat, lng = gen_coord(i)
    places.append({
        "name": p["name"],
        "lat": lat,
        "lng": lng,
        "type": p["type"],
        "rating": p["rating"],
        "price": p["price"],
        "desc": p["comment"]
    })


# =========================
# webhook（唯一版本）
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
                {"type":"text","text":"🎡 會員功能"},
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

        # 🗺️ 地圖
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

    except:
        return "OK"


# =========================
# map
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
body {{ margin:0; display:flex; height:100vh; }}
#map {{ flex:1; }}
#panel {{ width:320px; overflow:auto; background:#fafafa; padding:10px; }}
.card {{ background:#fff; margin:6px; padding:8px; border-radius:10px; cursor:pointer; }}
</style>

</head>

<body>

<div id="map"></div>
<div id="panel"><h3>致理美食</h3></div>

<script>

const map = L.map('map').setView([25.0250, 121.4630], 18);

L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);

const places = {json.dumps(places, ensure_ascii=False)};

places.forEach(p => {{
    L.marker([p.lat,p.lng]).addTo(map)
    .bindPopup(`<b>${{p.name}}</b><br>${{p.desc}}`);

    document.getElementById("panel").innerHTML += `
    <div class="card" onclick="map.setView([${{p.lat}},${{p.lng}}],19)">
        <b>${{p.name}}</b><br>
        ⭐ ${{p.rating}} | ${{p.price}}<br>
        ${{p.desc}}
    </div>`;
}});

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
