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
# 📌 美食資料
# =========================
places = [
    {"name":"致理飯糰","lat":25.0231,"lng":121.4675,"type":"台式","rating":4.3,"reviews":120,"hours":"06:30–10:30"},
    {"name":"小陳滷味","lat":25.0232,"lng":121.4676,"type":"台式","rating":4.5,"reviews":210,"hours":"17:00–23:30"},
    {"name":"文化小吃","lat":25.0233,"lng":121.4674,"type":"台式","rating":4.1,"reviews":98,"hours":"10:00–20:00"},

    {"name":"麥當勞文化店","lat":25.0236,"lng":121.4679,"type":"早午餐","rating":4.2,"reviews":980,"hours":"24小時"},
    {"name":"晨間廚房","lat":25.0232,"lng":121.4672,"type":"早午餐","rating":4.1,"reviews":340,"hours":"06:00–14:00"},

    {"name":"Is Pasta","lat":25.0233,"lng":121.4675,"type":"日式義式","rating":4.3,"reviews":210,"hours":"11:00–21:30"},
    {"name":"Sukiya","lat":25.0234,"lng":121.4676,"type":"日式義式","rating":4.4,"reviews":410,"hours":"24小時"},

    {"name":"韓鼓韓式料理","lat":25.0230,"lng":121.4670,"type":"異國","rating":4.3,"reviews":320,"hours":"11:00–21:00"},

    {"name":"路易莎","lat":25.0233,"lng":121.4673,"type":"咖啡","rating":4.4,"reviews":620,"hours":"07:00–21:00"},

    {"name":"阿耀臭豆腐","lat":25.0141,"lng":121.4621,"type":"宵夜","rating":4.2,"reviews":180,"hours":"17:00–00:30"},
]


# =========================
# LINE webhook（轉盤完全不動）
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()

    try:
        event = body["events"][0]

        if event["message"]["type"] != "text":
            return "OK"

        reply_token = event["replyToken"]
        msg = event["message"]["text"]

        # 🎡 轉盤（不動）
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
                "type": "template",
                "altText": "美食地圖",
                "template": {
                    "type": "buttons",
                    "text": "🍜 致理校園美食地圖已開啟",
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
# 🌍 校園美食地圖（APP版 UI）
# =========================
@app.route("/map")
def map_page():

    categories = ["台式","早午餐","日式義式","異國","咖啡","宵夜"]

    html = """
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>致理校園美食地圖</title>

    <style>
        body{
            margin:0;
            font-family: -apple-system, BlinkMacSystemFont, "Noto Sans TC";
            background:#f4f6f8;
        }

        /* 🔥 APP頂部 */
        .header{
            background:linear-gradient(135deg,#ff6b6b,#ff9f43);
            color:white;
            padding:22px 16px;
            font-size:22px;
            font-weight:800;
            text-align:center;
        }

        .sub{
            font-size:13px;
            opacity:0.9;
            margin-top:4px;
        }

        /* 🔍 搜尋 */
        .search{
            padding:10px;
        }

        input{
            width:100%;
            padding:12px;
            border-radius:12px;
            border:none;
            font-size:16px;
        }

        /* 🧭 分類 */
        .tabs{
            display:flex;
            overflow-x:auto;
            padding:10px;
            gap:8px;
        }

        .tab{
            padding:8px 12px;
            background:white;
            border-radius:20px;
            font-size:14px;
            white-space:nowrap;
            box-shadow:0 2px 5px rgba(0,0,0,0.05);
        }

        /* 卡片 */
        .card{
            background:white;
            margin:10px;
            padding:14px;
            border-radius:16px;
            box-shadow:0 3px 10px rgba(0,0,0,0.08);
        }

        .name{
            font-size:20px;
            font-weight:800;
        }

        .meta{
            font-size:14px;
            color:#666;
            margin-top:6px;
            line-height:1.6;
        }

        .btn{
            display:inline-block;
            margin-top:10px;
            padding:8px 12px;
            background:#00b894;
            color:white;
            border-radius:10px;
            text-decoration:none;
            font-size:14px;
        }
    </style>

    <script>
        function filterType(type){
            let cards = document.getElementsByClassName("card");
            for(let c of cards){
                if(type === "全部" || c.dataset.type === type){
                    c.style.display = "block";
                }else{
                    c.style.display = "none";
                }
            }
        }

        function searchFood(){
            let q = document.getElementById("search").value.toLowerCase();
            let cards = document.getElementsByClassName("card");

            for(let c of cards){
                let name = c.dataset.name.toLowerCase();
                c.style.display = name.includes(q) ? "block" : "none";
            }
        }
    </script>

    </head>

    <body>

    <div class="header">
        🍜 致理校園美食地圖
        <div class="sub">不知道吃什麼就打開這個</div>
    </div>

    <div class="search">
        <input id="search" onkeyup="searchFood()" placeholder="搜尋店名...">
    </div>

    <div class="tabs">
        <div class="tab" onclick="filterType('全部')">全部</div>
        <div class="tab" onclick="filterType('台式')">台式</div>
        <div class="tab" onclick="filterType('早午餐')">早午餐</div>
        <div class="tab" onclick="filterType('日式義式')">日式義式</div>
        <div class="tab" onclick="filterType('異國')">異國</div>
        <div class="tab" onclick="filterType('咖啡')">咖啡</div>
        <div class="tab" onclick="filterType('宵夜')">宵夜</div>
    </div>
    """

    for x in places:

        maps = f"https://www.google.com/maps/search/?api=1&query={x['name']}"

        html += f"""
        <div class="card" data-type="{x['type']}" data-name="{x['name']}">

            <div class="name">{x['name']}</div>

            <div class="meta">
                ⭐ {x['rating']} / {x['reviews']}則<br>
                🕒 {x['hours']}<br>
                📍 {x['type']}
            </div>

            <a class="btn" target="_blank" href="{maps}">
                Google Maps
            </a>

        </div>
        """

    html += "</body></html>"
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
