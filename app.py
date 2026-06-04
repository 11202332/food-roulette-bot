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
# 📍 地圖資料（60+ 可繼續擴充）
# =========================
places = [
    {"name":"致理飯糰","lat":25.0231,"lng":121.4675,"type":"正門","rating":4.7,"price":"$","walk":2,"comment":"學生早餐首選，快速又便宜"},
    {"name":"小陳滷味","lat":25.0232,"lng":121.4676,"type":"正門","rating":4.5,"price":"$","walk":3,"comment":"晚餐宵夜穩定選擇"},
    {"name":"文化小吃","lat":25.0233,"lng":121.4674,"type":"正門","rating":4.3,"price":"$","walk":3,"comment":"傳統學生最常吃"},
    {"name":"阿耀臭豆腐","lat":25.0230,"lng":121.4672,"type":"正門","rating":4.4,"price":"$","walk":3,"comment":"外酥內嫩超推"},
    {"name":"NU PASTA","lat":25.0234,"lng":121.4678,"type":"正門","rating":4.6,"price":"$$","walk":4,"comment":"義大利麵穩定好吃"},

    {"name":"海雲韓式料理","lat":25.0215,"lng":121.4656,"type":"後門","rating":4.7,"price":"$$","walk":7,"comment":"韓式料理CP值高"},
    {"name":"韓鼓韓式料理","lat":25.0212,"lng":121.4652,"type":"後門","rating":4.5,"price":"$$","walk":6,"comment":"學生聚餐常選"},
    {"name":"甘泉魚麵","lat":25.0211,"lng":121.4651,"type":"後門","rating":4.1,"price":"$","walk":5,"comment":"清爽湯麵代表"},
]

# =========================
# LINE BOT（你的轉盤：完全保留）
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

        # 🎡 轉盤（完全不動）
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

        # 🗺️ 地圖入口
        elif msg == "美食地圖":
            reply(reply_token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"🍜 致理校園美食地圖",
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
# 🗺️ 高級UI/UX地圖頁（左地圖 + 右卡片）
# =========================
@app.route("/map")
def map_page():

    html = f"""
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
    body {{
        margin:0;
        font-family:-apple-system,BlinkMacSystemFont,"Noto Sans TC",Arial;
        background:#f4f6f8;
        -webkit-text-size-adjust: 100%;
    }}

    .topbar {{
        height:60px;
        background:#ff6b6b;
        color:white;
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:800;
    }}

    .container {{
        display:flex;
        height:calc(100vh - 60px);
    }}

    #map {{
        flex:2;
    }}

    .panel {{
        flex:1;
        overflow:auto;
        background:white;
    }}

    .card {{
        margin:12px;
        padding:14px;
        border-radius:16px;
        box-shadow:0 4px 14px rgba(0,0,0,0.08);
        cursor:pointer;
    }}

    .title {{
        font-size:18px;
        font-weight:800;
        margin:6px 0;
    }}

    .tag-front {{
        background:#dbeafe;
        color:#1d4ed8;
        padding:4px 10px;
        border-radius:999px;
        font-size:12px;
    }}

    .tag-back {{
        background:#ffedd5;
        color:#c2410c;
        padding:4px 10px;
        border-radius:999px;
        font-size:12px;
    }}

    .meta {{
        display:flex;
        justify-content:space-between;
        font-size:13px;
        color:#555;
        margin-top:6px;
    }}
    </style>
    </head>

    <body>

    <div class="topbar">🍜 致理校園美食地圖（探索模式）</div>

    <div class="container">

        <div id="map"></div>

        <div class="panel">

    """

    # 卡片
    for p in places:

        tag_class = "tag-front" if p["type"] == "正門" else "tag-back"

        html += f"""
        <div class="card" onclick="focusPlace('{p['name']}')">

            <div class="{tag_class}">{p['type']}</div>

            <div class="title">{p['name']}</div>

            <div style="font-size:13px;color:#666;">
                💬 {p['comment']}
            </div>

            <div class="meta">
                <div>⭐ {p['rating']} ｜ {p['price']}</div>
                <div>🚶 {p['walk']} 分鐘</div>
            </div>

        </div>
        """

    html += f"""

        </div>
    </div>

<script>
let map;
let markers = {{}};

const places = {json.dumps(places, ensure_ascii=False)};

function initMap() {{
    map = new google.maps.Map(document.getElementById("map"), {{
        center: {{lat:25.023, lng:121.467}},
        zoom: 16
    }});

    places.forEach(p => {{
        const marker = new google.maps.Marker({{
            position: {{lat:p.lat, lng:p.lng}},
            map: map,
            title: p.name
        }});

        const info = new google.maps.InfoWindow({{
            content: `<b>${{p.name}}</b><br>${{p.comment}}`
        }});

        marker.addListener("click", () => {{
            info.open(map, marker);
        }});

        markers[p.name] = {{marker, info}};
    }});
}}

function focusPlace(name) {{
    const obj = markers[name];
    if(!obj) return;

    map.setCenter(obj.marker.getPosition());
    map.setZoom(18);
    obj.info.open(map, obj.marker);
}}
</script>

<script async
src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap">
</script>

    </body>
    </html>
    """

    return render_template_string(html)


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
