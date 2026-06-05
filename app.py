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
{"name":"栄次郎燒肉","rating":4.7,"price":"$200-400","area":"文化"},
{"name":"FlagPasta","rating":4.5,"price":"$200-400","area":"陽明"},
{"name":"小食。候","rating":4.3,"price":"$200-400","area":"陽明"},
{"name":"義匠湯麵","rating":4.8,"price":"$200-400","area":"陽明"},
{"name":"鄉親小吃","rating":4.6,"price":"$1-200","area":"幸福"},
{"name":"逸麵鍋燒","rating":4.9,"price":"$1-200","area":"新海"},
{"name":"is pasta","rating":4.3,"price":"$200-400","area":"文化"},
{"name":"吉飽早餐","rating":4.0,"price":"$1-200","area":"文化"},
{"name":"致理飯糰","rating":4.7,"price":"$1-200","area":"文化"},
{"name":"小松拉麵","rating":4.5,"price":"$1-200","area":"陽明"},
{"name":"一京咖哩","rating":4.6,"price":"$1-200","area":"陽明"},
{"name":"MABO POKE","rating":4.3,"price":"$1-200","area":"文化"},
{"name":"海雲韓式","rating":4.7,"price":"$400-600","area":"陽明"},
{"name":"紅居館","rating":4.8,"price":"$400-800","area":"新海"}
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

        # 🎡 轉盤（完整保留）
        if msg == "美食轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 美食轉盤開啟"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        # 🗺️ 地圖入口
        elif msg == "美食地圖":
            reply(reply_token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"致理手繪美食地圖",
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
# 🗺️ 手繪地圖（核心）
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

/* 左清單 */
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
    border-radius:12px;
    box-shadow:0 2px 5px rgba(0,0,0,0.08);
}

/* 右地圖 */
#map{
    flex:1;
    position:relative;
    background:#f3efe6;
}

/* 致理中心 */
.center{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    background:white;
    padding:6px 10px;
    border-radius:10px;
    font-weight:bold;
    color:#c0392b;
}

/* 十字街道 */
.roadV{
    position:absolute;
    width:6px;
    height:100%;
    left:50%;
    background:#d6c6a5;
    transform:translateX(-50%);
    opacity:0.4;
}

.roadH{
    position:absolute;
    height:6px;
    width:100%;
    top:50%;
    background:#d6c6a5;
    transform:translateY(-50%);
    opacity:0.4;
}

/* 標示街道 */
.street{
    position:absolute;
    font-size:13px;
    font-weight:bold;
    color:#555;
}

.culture{ top:10%; left:48%; }
.yangming{ top:50%; right:5%; }
.xinhai{ bottom:10%; left:48%; }
.happy{ top:50%; left:5%; }

/* 店家 */
.shop{
    position:absolute;
    transform:translate(-50%,-50%);
    text-align:center;
}

.pin{
    width:12px;
    height:12px;
    background:#ff6b6b;
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

<div id="panel">
<h3>🍜 致理美食清單</h3>
"""

    for p in places:
        html += f"""
        <div class="card">
            <b>{p['name']}</b><br>
            ⭐ {p['rating']}<br>
            📍 {p['area']}路線
        </div>
        """

    html += """
</div>

<div id="map">

<div class="roadV"></div>
<div class="roadH"></div>

<div class="center">🎓 致理科技大學</div>

<div class="street culture">文化路</div>
<div class="street yangming">陽明街</div>
<div class="street xinhai">新海路</div>
<div class="street happy">幸福路</div>
"""

    # =========================
    # 🧭 重點：手繪分布（穩定版）
    # =========================
    for i, p in enumerate(places):

        if p["area"] == "文化":
            top = 30 + (i % 4) * 6
            left = 50 + (i % 3 - 1) * 8

        elif p["area"] == "陽明":
            top = 50 + (i % 4 - 2) * 6
            left = 75 + (i % 3) * 5

        elif p["area"] == "新海":
            top = 75 + (i % 4) * 5
            left = 50 + (i % 3 - 1) * 8

        else:  # 幸福
            top = 50 + (i % 4 - 2) * 6
            left = 25 + (i % 3) * 5

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
