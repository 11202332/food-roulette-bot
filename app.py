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
# 🍜 完整店家資料（升級版）
# =========================
places = [
{"name":"栄次郎燒肉","rating":4.7,"price":"$200-400","type":"燒肉","area":"文化","comment":"肉香很爽但荷包會痛"},
{"name":"FlagPasta","rating":4.5,"price":"$200-400","type":"義大利麵","area":"陽明","comment":"穩定不踩雷"},
{"name":"小食。候","rating":4.3,"price":"$200-400","type":"咖啡","area":"陽明","comment":"安靜讀書咖啡廳"},
{"name":"義匠湯麵","rating":4.8,"price":"$200-400","type":"湯麵","area":"陽明","comment":"湯頭很強"},
{"name":"鄉親小吃","rating":4.6,"price":"$1-200","type":"小吃","area":"幸福","comment":"便宜又飽"},
{"name":"逸麵鍋燒","rating":4.9,"price":"$1-200","type":"鍋燒","area":"新海","comment":"學生最愛"},
{"name":"is pasta","rating":4.3,"price":"$200-400","type":"義大利麵","area":"文化","comment":"聚餐安全牌"},
{"name":"吉飽早餐","rating":4.0,"price":"$1-200","type":"早餐","area":"文化","comment":"早八救星"},
{"name":"致理飯糰","rating":4.7,"price":"$1-200","type":"早餐","area":"文化","comment":"超大顆飯糰"},
{"name":"小松拉麵","rating":4.5,"price":"$1-200","type":"拉麵","area":"陽明","comment":"CP值高"},
{"name":"一京咖哩","rating":4.6,"price":"$1-200","type":"咖哩","area":"陽明","comment":"濃郁系"},
{"name":"MABO POKE","rating":4.3,"price":"$1-200","type":"健康","area":"文化","comment":"清爽沙拉飯"},
{"name":"海雲韓式","rating":4.7,"price":"$400-600","type":"韓式","area":"陽明","comment":"炸雞很讚"},
{"name":"紅居館","rating":4.8,"price":"$400-800","type":"台菜","area":"新海","comment":"聚餐首選"}
]


# =========================
# LINE webhook（轉盤 + 地圖）
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
                {"type":"text","text":"🎡 美食轉盤"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        # 🗺️ 地圖
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
# 🗺️ 手繪地圖（最終美化版）
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
    background:#f7f3ea;
}

/* 左清單 */
#panel{
    width:330px;
    background:#fff8ee;
    padding:12px;
    overflow:auto;
}

.card{
    background:linear-gradient(135deg,#fff,#fff7ee);
    margin:8px 0;
    padding:10px;
    border-radius:14px;
    box-shadow:0 3px 10px rgba(0,0,0,0.08);
    transition:0.2s;
}

.card:hover{
    transform:scale(1.02);
}

/* 地圖 */
#map{
    flex:1;
    position:relative;
    background:#f1eadf;
}

/* 致理中心 */
.center{
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    background:white;
    padding:6px 12px;
    border-radius:10px;
    font-weight:bold;
    color:#c0392b;
    box-shadow:0 2px 6px rgba(0,0,0,0.15);
}

/* 十字道路 */
.roadV{
    position:absolute;
    width:6px;
    height:100%;
    left:50%;
    background:#cdb79e;
    opacity:0.5;
    transform:translateX(-50%);
}

.roadH{
    position:absolute;
    height:6px;
    width:100%;
    top:50%;
    background:#cdb79e;
    opacity:0.5;
}

/* 街道標示 */
.street{
    position:absolute;
    font-size:13px;
    font-weight:bold;
    color:#555;
}

.culture{ top:8%; left:48%; }
.yangming{ top:50%; right:5%; }
.xinhai{ bottom:8%; left:48%; }
.happy{ top:50%; left:5%; }

/* 店家點 */
.food{
    position:absolute;
    transform:translate(-50%,-50%);
    text-align:center;
}

/* 顏色分類 */
.red{ background:#ff6b6b; }
.green{ background:#51cf66; }
.blue{ background:#4dabf7; }
.brown{ background:#d9a066; }

.pin{
    width:13px;
    height:13px;
    border-radius:50%;
    border:2px solid white;
    margin:auto;
    box-shadow:0 2px 6px rgba(0,0,0,0.2);
}

.label{
    font-size:10px;
    background:white;
    padding:2px 6px;
    border-radius:8px;
    box-shadow:0 1px 4px rgba(0,0,0,0.1);
}
</style>

</head>

<body>

<div id="panel">
<h3>🍜 致理美食清單</h3>
"""

    # 左側清單
    for p in places:
        html += f"""
        <div class="card">
            <b>{p['name']}</b><br>
            ⭐ {p['rating']} | {p['price']}<br>
            📍 {p['comment']}
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
    # 🎯 地圖分布 + 顏色
    # =========================
    for i, p in enumerate(places):

        # 顏色分類
        if p["type"] in ["早餐"]:
            color = "green"
        elif p["type"] in ["燒肉","台菜","韓式"]:
            color = "red"
        elif p["type"] in ["咖啡","健康"]:
            color = "blue"
        else:
            color = "brown"

        # 區域分布
        if p["area"] == "文化":
            top = 30 + (i % 4) * 6
            left = 50 + (i % 3 - 1) * 8

        elif p["area"] == "陽明":
            top = 50 + (i % 4 - 2) * 6
            left = 75 + (i % 3) * 5

        elif p["area"] == "新海":
            top = 75 + (i % 4) * 5
            left = 50 + (i % 3 - 1) * 8

        else:
            top = 50 + (i % 4 - 2) * 6
            left = 25 + (i % 3) * 5

        html += f"""
        <div class="food {color}" style="top:{top}%;left:{left}%;">
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
