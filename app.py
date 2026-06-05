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
places = [
{"name":"栄次郎個人燒肉","rating":4.7,"price":"$200-400","type":"燒肉","comment":"自己烤肉很爽但錢包會痛"},
{"name":"FlagPasta","rating":4.5,"price":"$200-400","type":"義大利麵","comment":"穩定不踩雷"},
{"name":"小食。候","rating":4.3,"price":"$200-400","type":"咖啡","comment":"安靜但容易客滿"},
{"name":"義匠義式湯麵","rating":4.8,"price":"$200-400","type":"義大利麵","comment":"湯麵很特別"},
{"name":"鄉親小吃","rating":4.6,"price":"$1-200","type":"小吃","comment":"便宜實在"},
{"name":"逸麵鍋燒","rating":4.9,"price":"$1-200","type":"鍋燒","comment":"湯頭超強"},
{"name":"is pasta","rating":4.3,"price":"$200-400","type":"義大利麵","comment":"學生聚餐常去"},
{"name":"吉飽早餐","rating":4.0,"price":"$1-200","type":"早餐","comment":"早八救星"},
{"name":"致理飯糰","rating":4.7,"price":"$1-200","type":"早餐","comment":"飯糰超大顆"},
{"name":"小松拉麵","rating":4.5,"price":"$1-200","type":"日式","comment":"平價拉麵"},
{"name":"一京咖哩","rating":4.6,"price":"$1-200","type":"咖哩","comment":"咖哩濃郁"},
{"name":"吳二麻辣鴨血","rating":4.4,"price":"$1-200","type":"麻辣","comment":"冬天必吃"},
{"name":"吉野烤肉飯","rating":3.8,"price":"$1-200","type":"便當","comment":"快速解決"},
{"name":"MABO POKE","rating":4.3,"price":"$1-200","type":"健康","comment":"清爽路線"},
{"name":"Café Wanderer","rating":4.4,"price":"$200-400","type":"咖啡","comment":"文青咖啡廳"},
{"name":"紅居館台菜","rating":4.8,"price":"$400-800","type":"台菜","comment":"聚餐用"},
{"name":"海雲韓式料理","rating":4.7,"price":"$400-600","type":"韓式","comment":"炸雞好吃"},
{"name":"NU PASTA","rating":4.6,"price":"$200-400","type":"義大利麵","comment":"穩定聚餐"},
{"name":"光東養茶","rating":4.7,"price":"$1-200","type":"飲料","comment":"茶味乾淨"},
{"name":"8鍋臭臭鍋","rating":3.9,"price":"$1-200","type":"火鍋","comment":"平價火鍋"},
{"name":"麻丹辣小火鍋","rating":4.9,"price":"$200-400","type":"火鍋","comment":"學生最愛"},
{"name":"牪嗑牛排","rating":4.3,"price":"$200-400","type":"牛排","comment":"學生牛排"},
{"name":"龍一海南雞","rating":4.6,"price":"$1-200","type":"便當","comment":"雞肉很嫩"},
]


# =========================
# LINE webhook
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
                {"type":"text","text":"🎡 開啟轉盤👇"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        elif msg == "加入會員":
            reply(reply_token, [
                {"type":"text","text":"📝 會員表單"},
                {"type":"text","text":"https://forms.gle/jYykimjWcX1rgYRW8"}
            ])

        # 🗺️ 地圖
        elif msg == "美食地圖":
            reply(reply_token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"致理美食地圖",
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
# 🗺️ 手繪美食地圖（你要的版本）
# =========================
@app.route("/map")
def map_page():

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>致理美食手繪地圖</title>

<style>
body{
    margin:0;
    display:flex;
    height:100vh;
    font-family:Arial;
}

/* 左側 */
#panel{
    width:320px;
    background:#fff8ee;
    padding:12px;
    overflow:auto;
}

.card{
    background:white;
    margin:8px 0;
    padding:10px;
    border-radius:14px;
    box-shadow:0 2px 6px rgba(0,0,0,0.08);
}

/* 右側手繪地圖 */
#map{
    flex:1;
    position:relative;
    background:#f5efe6;
}

/* 區域 */
.zone{
    position:absolute;
    font-size:16px;
    font-weight:bold;
    color:#6b4f3a;
    background:rgba(255,255,255,0.7);
    padding:4px 10px;
    border-radius:10px;
}

.z1{top:10%;left:15%;}
.z2{top:45%;left:30%;}
.z3{top:75%;left:45%;}

/* 店家 */
.shop{
    position:absolute;
    transform:translate(-50%,-50%);
    text-align:center;
}

.pin{
    width:14px;
    height:14px;
    background:#ff6b6b;
    border-radius:50%;
    border:2px solid white;
    margin:auto;
}

.label{
    font-size:11px;
    background:white;
    padding:2px 6px;
    border-radius:8px;
}
</style>

</head>

<body>

<div id="panel">
<h3>🍜 致理美食清單</h3>
"""

    for p in places:
        html += f"""
        <div class="card">
            <b>{p['name']}</b><br>
            ⭐ {p['rating']} | {p['price']}<br>
            {p['comment']}
        </div>
        """

    html += """
</div>

<div id="map">

<div class="zone z1">文化路</div>
<div class="zone z2">陽明街</div>
<div class="zone z3">新海路</div>
"""

    # 固定分區（乾淨版）
    for i, p in enumerate(places):

        zone = i % 3

        if zone == 0:
            top = 15 + (i % 8) * 6
            left = 15 + (i % 5) * 6
        elif zone == 1:
            top = 45 + (i % 8) * 5
            left = 30 + (i % 5) * 6
        else:
            top = 70 + (i % 8) * 4
            left = 45 + (i % 5) * 6

        html += f"""
        <div class="shop" style="top:{top}%;left:{left}%;">
            <div class="pin"></div>
            <div class="label">{p['name']}</div>
        </div>
        """

    html += """
</div>

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
