from flask import Flask, request, render_template_string
import requests, os, json

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
LINE_API = "https://api.line.me/v2/bot/message/reply"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_TOKEN}"
}

def reply(token, messages):
    requests.post(LINE_API, headers=headers, data=json.dumps({
        "replyToken": token,
        "messages": messages
    }))


# =========================
# 🍜 完整店家（含連結）
# =========================
places = [
{"name":"栄次郎燒肉","area":"文化路","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
{"name":"FlagPasta","area":"陽明街","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
{"name":"小食。候","area":"陽明街","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
{"name":"義匠湯麵","area":"陽明街","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
{"name":"鄉親小吃","area":"幸福路","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
{"name":"逸麵鍋燒","area":"新海路","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
{"name":"致理飯糰","area":"文化路","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
{"name":"吉飽早餐","area":"文化路","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
{"name":"MABO POKE","area":"文化路","url":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9"},
{"name":"海雲韓式","area":"自由路","url":"https://maps.app.goo.gl/gQbAeUjs4MwnYePi7"},
]


# =========================
# LINE webhook（轉盤完全不動）
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()

    try:
        event = body["events"][0]
        msg = event["message"]["text"]
        token = event["replyToken"]

        # 🎡 轉盤（100%不動）
        if msg == "美食轉盤":
            reply(token, [
                {"type":"text","text":"🎡 轉盤開啟"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        # 🗺️ 地圖
        elif msg == "美食地圖":
            reply(token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"致理美食地圖",
                    "actions":[{
                        "type":"uri",
                        "label":"打開地圖",
                        "uri":"https://food-roulette-bot.onrender.com/map"
                    }]
                }
            }])

        else:
            reply(token,[{"type":"text","text":"收到：" + msg}])

        return "OK"
    except:
        return "OK"


# =========================
# 🗺️ 真正「看得懂版本」
# =========================
@app.route("/map")
def map_page():

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>致理美食地圖</title>

<style>
body{
    margin:0;
    display:flex;
    height:100vh;
    font-family:Arial;
}

/* 左邊清單（保留 + 可點） */
#panel{
    width:340px;
    background:#fff8ee;
    padding:12px;
    overflow:auto;
}

.card{
    background:white;
    margin:8px 0;
    padding:10px;
    border-radius:12px;
    box-shadow:0 2px 6px rgba(0,0,0,0.08);
}

.card a{
    text-decoration:none;
    color:#333;
}

/* 右邊地圖 */
#map{
    flex:1;
    position:relative;
    background:#f2e6d3;
}

/* 致理中心 */
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

/* 四個方向（重點：讓人看懂） */
.zone{
    position:absolute;
    font-weight:bold;
    font-size:13px;
    background:rgba(255,255,255,0.7);
    padding:4px 8px;
    border-radius:8px;
}

.north{top:5%;left:50%;transform:translateX(-50%);}
.south{bottom:5%;left:50%;transform:translateX(-50%);}
.east{top:50%;right:5%;}
.west{top:50%;left:5%;}

/* 店家點 */
.shop{
    position:absolute;
    transform:translate(-50%,-50%);
    text-align:center;
}

.dot{
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
    white-space:nowrap;
}
</style>
</head>

<body>

<div id="panel">
<h3>🍜 致理美食清單</h3>
"""

    # =========================
    # 左側：可點 Google Maps（你要的）
    # =========================
    for p in places:
        html += f"""
        <div class="card">
            <a href="{p['url']}" target="_blank">
                <b>{p['name']}</b><br>
                📍 {p['area']}
            </a>
        </div>
        """

    html += """
</div>

<div id="map">

<div class="center">🎓 致理科技大學</div>

<div class="zone north">北｜早餐區</div>
<div class="zone south">南｜小吃區</div>
<div class="zone east">東｜文化路</div>
<div class="zone west">西｜陽明街</div>
"""

    # =========================
    # 右邊：真正「固定邏輯定位」
    # =========================
    for i, p in enumerate(places):

        if p["area"] == "文化路":
            top = 40 + (i % 4) * 5
            left = 70 + (i % 2) * 5

        elif p["area"] == "陽明街":
            top = 35 + (i % 4) * 5
            left = 75

        elif p["area"] == "新海路":
            top = 75
            left = 55 + (i % 3) * 5

        elif p["area"] == "幸福路":
            top = 80
            left = 30 + (i % 3) * 5

        else:
            top, left = 50, 50

        html += f"""
        <div class="shop" style="top:{top}%;left:{left}%;">
            <div class="dot"></div>
            <div class="label">{p['name']}</div>
        </div>
        """

    html += """
</div>

</body>
</html>
"""

    return render_template_string(html)


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
