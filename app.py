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
    requests.post(
        LINE_API,
        headers=headers,
        data=json.dumps({"replyToken": token, "messages": messages})
    )

# =========================
# 🍜 店家（保留但簡化顯示）
# =========================
places = [
{"name":"栄次郎燒肉","area":"東","type":"燒肉","rating":4.7,"url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
{"name":"FlagPasta","area":"東","type":"義大利麵","rating":4.5,"url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
{"name":"小食。候","area":"東","type":"咖啡","rating":4.3,"url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
{"name":"義匠湯麵","area":"東","type":"麵食","rating":4.8,"url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},

{"name":"致理飯糰","area":"北","type":"早餐","rating":4.7,"url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
{"name":"吉飽早餐","area":"北","type":"早餐","rating":4.0,"url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},

{"name":"鄉親小吃","area":"南","type":"小吃","rating":4.6,"url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
{"name":"逸麵鍋燒","area":"南","type":"火鍋","rating":4.9,"url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},

{"name":"海雲韓式","area":"西","type":"韓式","rating":4.7,"url":"https://maps.app.goo.gl/gQbAeUjs4MwnYePi7"},
{"name":"紅居館","area":"南","type":"台菜","rating":4.8,"url":"https://maps.app.goo.gl/pM2ksGeQ3Dw59zup6"},
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

        # 🎡 轉盤（完全保留）
        if msg == "美食轉盤":
            reply(token, [
                {"type":"text","text":"🎡 開啟轉盤"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        # 🗺️ 地圖
        elif msg == "美食地圖":
            reply(token, [{
                "type":"template",
                "altText":"美食地圖",
                "template":{
                    "type":"buttons",
                    "text":"手機版致理美食地圖",
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
# 📱 手機專用地圖（重點）
# =========================
@app.route("/map")
def map_page():

    html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>致理美食地圖</title>

<style>
body{
    margin:0;
    font-family:Arial;
    background:#f6f1e7;
}

/* 地圖主畫面（手機滑動） */
#map{
    position:relative;
    width:100%;
    height:100vh;
    background:linear-gradient(#f0e6d6,#e9dcc6);
}

/* 中心 */
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

/* 區域 */
.zone{
    position:absolute;
    font-size:14px;
    font-weight:bold;
    color:#444;
}

.north{top:5%;left:50%;transform:translateX(-50%);}
.south{bottom:5%;left:50%;transform:translateX(-50%);}
.east{top:50%;right:5%;}
.west{top:50%;left:5%;}

/* 店家點（手機優化） */
.pin{
    position:absolute;
    transform:translate(-50%,-50%);
    text-align:center;
}

.dot{
    width:12px;height:12px;
    background:#ff6b6b;
    border-radius:50%;
    border:2px solid white;
    margin:auto;
}

.label{
    font-size:10px;
    background:white;
    padding:2px 4px;
    border-radius:6px;
}
</style>
</head>

<body>

<div id="map">

<div class="center">🎓 致理科技大學</div>

<div class="zone north">北｜早餐區</div>
<div class="zone south">南｜小吃區</div>
<div class="zone east">東｜文化路</div>
<div class="zone west">西｜陽明街</div>
"""

    # =========================
    # 📍 手機清楚分區（不亂飄）
    # =========================
    for i, p in enumerate(places):

        if p["area"] == "北":
            top = 15 + i*2
            left = 50 + (i%3)*10

        elif p["area"] == "南":
            top = 75 + i*2
            left = 50 + (i%3)*10

        elif p["area"] == "東":
            top = 50 + (i%3)*8
            left = 75

        else:
            top = 50 + (i%3)*8
            left = 25

        html += f"""
        <a href="{p['url']}" target="_blank">
        <div class="pin" style="top:{top}%;left:{left}%;">
            <div class="dot"></div>
            <div class="label">{p['name']}</div>
        </div>
        </a>
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
