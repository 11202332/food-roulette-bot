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
# ⭐ 會員系統（超簡版）
# =========================
members = set()  # 存 userId


# =========================
# 🍜 店家資料
# =========================
places = [
{"name":"栄次郎燒肉","area":"文化路","rating":"4.7","price":"$200-400","comment":"個人燒肉很熱門","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
{"name":"FlagPasta","area":"陽明街","rating":"4.5","price":"$200-400","comment":"學生愛店","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
{"name":"小食。候","area":"陽明街","rating":"4.3","price":"$200-400","comment":"文青咖啡","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
{"name":"義匠湯麵","area":"陽明街","rating":"4.8","price":"$200-400","comment":"義式湯麵","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
{"name":"鄉親小吃","area":"幸福路","rating":"4.6","price":"$1-200","comment":"平價小吃","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
{"name":"逸麵鍋燒","area":"新海路","rating":"4.9","price":"$1-200","comment":"學生最推","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
{"name":"致理飯糰","area":"文化路","rating":"4.7","price":"$1-200","comment":"早餐人氣","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
{"name":"吉飽早餐","area":"文化路","rating":"4.0","price":"$1-200","comment":"便宜早餐","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
{"name":"MABO POKE","area":"文化路","rating":"4.3","price":"$1-200","comment":"健康餐","url":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9"},
{"name":"海雲韓式","area":"自由路","rating":"4.7","price":"$400-600","comment":"韓式料理","url":"https://maps.app.goo.gl/gQbAeUjs4MwnYePi7"},
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
        token = event["replyToken"]
        user_id = event["source"]["userId"]

        # =========================
        # 🎡 轉盤（會員檢查）
        # =========================
        if msg == "美食轉盤":

            if user_id in members:
                reply(token, [
                    {"type":"text","text":"🎡 轉盤開啟"},
                    {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
                ])
            else:
                reply(token, [
                    {"type":"text","text":"⚠️ 你還不是會員"},
                    {"type":"text","text":"請先填寫表單加入會員👇"},
                    {"type":"text","text":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform?usp=header"}
                ])

        # =========================
        # 🧾 加入會員指令（你可以測試用）
        # =========================
        elif msg == "加入會員":
            members.add(user_id)
            reply(token,[{"type":"text","text":"✅ 已加入會員（測試用）"}])

        # =========================
        # 🗺️ 地圖
        # =========================
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
# 🗺️ 地圖頁
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
body{margin:0;font-family:Arial;display:flex;}

@media(max-width:768px){
 body{flex-direction:column;}
 #panel{width:100%!important;height:45vh;}
 #map{height:55vh;}
}

#panel{
 width:340px;
 background:#fff8ee;
 padding:12px;
 overflow:auto;
}

.card{
 background:white;
 margin:10px 0;
 padding:10px;
 border-radius:12px;
 box-shadow:0 2px 6px rgba(0,0,0,0.08);
}

#map{
 flex:1;
 position:relative;
 background:#f3e3cc;
}

.center{
 position:absolute;
 top:50%;left:50%;
 transform:translate(-50%,-50%);
 background:white;
 padding:10px;
 border-radius:12px;
 font-weight:bold;
}

.shop{
 position:absolute;
 transform:translate(-50%,-50%);
 text-align:center;
}

.dot{
 width:12px;height:12px;
 background:#ff4d4d;
 border-radius:50%;
 border:2px solid white;
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
<h3>🍜 美食清單</h3>
"""

    for p in places:
        html += f"""
        <div class="card">
            <b>{p['name']}</b><br>
            ⭐ {p['rating']} ｜ 💰 {p['price']}<br>
            💬 {p['comment']}<br>
            <a href="{p['url']}" target="_blank">📍 MAP</a>
        </div>
        """

    html += """
</div>

<div id="map">
<div class="center">🎓 致理科技大學</div>
"""

    for i, p in enumerate(places):

        base = {
            "文化路": (40, 60),
            "陽明街": (35, 80),
            "新海路": (75, 55),
            "幸福路": (80, 30),
            "自由路": (55, 85)
        }

        top, left = base.get(p["area"], (50,50))
        top += (i % 3) * 4
        left += (i % 2) * 4

        html += f"""
        <a href="{p['url']}" target="_blank">
        <div class="shop" style="top:{top}%;left:{left}%;">
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
