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
# 🍜 店家資料（精簡但完整保留）
# =========================
places = [
{"name":"栄次郎個人燒肉","area":"文化路","rating":4.7},
{"name":"FlagPasta","area":"陽明街","rating":4.5},
{"name":"小食。候","area":"陽明街","rating":4.3},
{"name":"義匠義式湯麵","area":"陽明街","rating":4.8},
{"name":"鄉親小吃","area":"幸福路","rating":4.6},
{"name":"逸麵鍋燒","area":"新海路","rating":4.9},
{"name":"is pasta","area":"文化路","rating":4.3},
{"name":"吉飽早餐","area":"文化路","rating":4.0},
{"name":"致理飯糰","area":"文化路","rating":4.7},
{"name":"小松拉麵","area":"自由路","rating":4.5},
{"name":"一京咖哩","area":"陽明街","rating":4.6},
{"name":"吳二麻辣鴨血","area":"文化路","rating":4.4},
{"name":"吉野烤肉飯","area":"文化路","rating":3.8},
{"name":"MABO POKE","area":"文化路","rating":4.3},
{"name":"Café Wanderer","area":"陽明街","rating":4.4},
{"name":"紅居館台菜","area":"漢生西路","rating":4.8},
{"name":"海雲韓式","area":"自由路","rating":4.7},
{"name":"NU PASTA","area":"陽明街","rating":4.6},
{"name":"光東養茶","area":"陽明街","rating":4.7},
{"name":"8鍋臭臭鍋","area":"漢生西路","rating":3.9},
{"name":"麻丹辣火鍋","area":"漢生西路","rating":4.9},
]


# =========================
# LINE Webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()

    try:
        event = body["events"][0]
        msg = event["message"]["text"]
        token = event["replyToken"]

        # 🎡 轉盤（完全保留）
        if msg == "美食轉盤":
            reply(token, [
                {"type":"text","text":"🎡 美食轉盤"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        # 🗺️ 地圖
        elif msg == "美食地圖":
            reply(token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"致理科技大學美食地圖",
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
            reply(token, [{"type":"text","text":"收到：" + msg}])

        return "OK"

    except:
        return "OK"


# =========================
# 🗺️ 手繪地圖（清楚分區版）
# =========================
@app.route("/map")
def map_page():

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>致理美食地圖</title>

<style>
body{
    margin:0;
    display:flex;
    height:100vh;
    font-family:Arial;
}

/* 左側清單 */
#panel{
    width:340px;
    background:#fff7ed;
    padding:12px;
    overflow-y:auto;
}

.card{
    background:white;
    margin:8px 0;
    padding:10px;
    border-radius:12px;
    box-shadow:0 2px 6px rgba(0,0,0,0.08);
}

/* 右側地圖 */
#map{
    flex:1;
    position:relative;
    background:#f3eadb;
}

/* 中心點 */
.center{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    background:white;
    padding:10px 14px;
    border-radius:12px;
    font-weight:bold;
    box-shadow:0 2px 8px rgba(0,0,0,0.2);
}

/* 街道標示 */
.street{
    position:absolute;
    font-size:13px;
    font-weight:bold;
    background:rgba(255,255,255,0.7);
    padding:4px 8px;
    border-radius:8px;
}

.s1{top:10%;left:50%;transform:translateX(-50%);} /* 文化路 */
.s2{top:45%;right:8%;} /* 陽明街 */
.s3{bottom:15%;left:55%;} /* 新海路 */
.s4{bottom:30%;left:20%;} /* 幸福路 */

/* 店家點 */
.shop{
    position:absolute;
    transform:translate(-50%,-50%);
    text-align:center;
}

.pin{
    width:12px;
    height:12px;
    background:#ff4d4d;
    border-radius:50%;
    border:2px solid white;
    margin:auto;
}

.label{
    font-size:10px;
    background:white;
    padding:2px 5px;
    border-radius:6px;
}
</style>
</head>

<body>

<!-- 左側清單 -->
<div id="panel">
<h3>🍜 致理美食清單</h3>
"""

    for p in places:
        html += f"""
        <div class="card">
            <b>{p['name']}</b><br>
            ⭐ {p['rating']}<br>
            {p['area']}
        </div>
        """

    html += """
</div>

<!-- 地圖 -->
<div id="map">

<div class="center">🎓 致理科技大學</div>

<div class="street s1">文化路一段</div>
<div class="street s2">陽明街</div>
<div class="street s3">新海路</div>
<div class="street s4">幸福路</div>
"""

    # =========================
    # 📍 固定區塊（不亂飄版本）
    # =========================
    for i, p in enumerate(places):

        if p["area"] == "文化路":
            top = 25 + (i % 5) * 5
            left = 50 + (i % 3) * 6

        elif p["area"] == "陽明街":
            top = 35 + (i % 5) * 5
            left = 75

        elif p["area"] == "新海路":
            top = 75
            left = 55 + (i % 4) * 6

        elif p["area"] == "幸福路":
            top = 80
            left = 30 + (i % 4) * 6

        elif p["area"] == "漢生西路":
            top = 60 + (i % 3) * 5
            left = 20

        else:
            top, left = 50, 50

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
