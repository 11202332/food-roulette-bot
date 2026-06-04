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
# 📍 60+ 校園美食（已擴充架構）
# =========================
places = [
    {"name":"致理飯糰","lat":25.0231,"lng":121.4675,"type":"正門","rating":4.7,"walk":2},
    {"name":"小陳滷味","lat":25.0232,"lng":121.4676,"type":"正門","rating":4.5,"walk":2},
    {"name":"文化小吃","lat":25.0233,"lng":121.4674,"type":"正門","rating":4.3,"walk":3},
    {"name":"阿耀臭豆腐","lat":25.0230,"lng":121.4672,"type":"正門","rating":4.4,"walk":3},
    {"name":"NU PASTA","lat":25.0234,"lng":121.4678,"type":"正門","rating":4.6,"walk":4},

    # 👉 後門區
    {"name":"韓鼓韓式料理","lat":25.0212,"lng":121.4652,"type":"後門","rating":4.5,"walk":6},
    {"name":"海雲韓式料理","lat":25.0215,"lng":121.4656,"type":"後門","rating":4.7,"walk":7},
    {"name":"甘泉魚麵","lat":25.0211,"lng":121.4651,"type":"後門","rating":4.1,"walk":5},
    {"name":"千尋味酸辣粉","lat":25.0213,"lng":121.4653,"type":"後門","rating":4.2,"walk":6},

    # 👉 外圍區（繼續擴充即可到 60+）
]

# =========================
# LINE Webhook（你的轉盤：完全保留）
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
# 🗺️ 超強 UI/UX 地圖頁（APP感核心）
# =========================
@app.route("/map")
def map_page():

    html = """
    <html>
    <head>
    <meta charset="utf-8">

    <style>
    body{
        margin:0;
        font-family:Arial;
        background:#f4f6f8;
        overflow:hidden;
    }

    /* 上方控制列 */
    .topbar{
        height:60px;
        background:#ff6b6b;
        color:white;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:18px;
        font-weight:bold;
    }

    /* 主畫面：左地圖 + 右卡片 */
    .container{
        display:flex;
        height:calc(100vh - 60px);
    }

    #map{
        flex:2;
        background:#ddd;
        position:relative;
    }

    .panel{
        flex:1;
        background:white;
        overflow:auto;
        padding:10px;
    }

    .card{
        background:white;
        margin:10px;
        padding:12px;
        border-radius:14px;
        box-shadow:0 2px 10px rgba(0,0,0,0.08);
        cursor:pointer;
        transition:0.2s;
    }

    .card:hover{
        transform:scale(1.02);
    }

    .tag{
        display:inline-block;
        padding:3px 8px;
        font-size:12px;
        background:#eee;
        border-radius:10px;
        margin-bottom:5px;
    }

    .filter{
        display:flex;
        gap:5px;
        padding:10px;
    }

    .btn{
        padding:6px 10px;
        border-radius:10px;
        border:0;
        background:#eee;
        cursor:pointer;
    }

    .btn:hover{
        background:#ddd;
    }

    </style>
    </head>

    <body>

    <div class="topbar">🍜 致理校園美食地圖（探索模式）</div>

    <div class="container">

        <div id="map">
            <iframe
                width="100%"
                height="100%"
                frameborder="0"
                src="https://www.google.com/maps?q=致理科技大學&output=embed">
            </iframe>
        </div>

        <div class="panel">

            <div class="filter">
                <button class="btn">正門</button>
                <button class="btn">後門</button>
                <button class="btn">5分鐘</button>
                <button class="btn">10分鐘</button>
            </div>

    """

    for p in places:
        maps_url = f"https://www.google.com/maps/search/?api=1&query={p['name']}"

        html += f"""
        <div class="card" onclick="window.open('{maps_url}')">
            <div class="tag">{p['type']}</div>
            <h3>{p['name']}</h3>
            ⭐ {p['rating']} ｜ 🚶 {p['walk']} 分鐘
        </div>
        """

    html += """
        </div>
    </div>

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
