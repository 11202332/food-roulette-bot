from flask import Flask, request, render_template_string
import requests
import os
import json
from collections import defaultdict

app = Flask(__name__)

LINE_TOKEN = os.environ.get("LINE_TOKEN")
LINE_API = "https://api.line.me/v2/bot/message/reply"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_TOKEN}" if LINE_TOKEN else ""
}

def reply(reply_token, messages):
    if not LINE_TOKEN:
        print("LINE_TOKEN missing")
        return

    try:
        requests.post(
            LINE_API,
            headers=headers,
            data=json.dumps({"replyToken": reply_token, "messages": messages}),
            timeout=5
        )
    except Exception as e:
        print("reply error:", e)


# =========================
# 🍜 完整店家資料（保留你全部）
# =========================
places = [
    {"name":"栄次郎個人燒肉—板橋文化店","address":"文化路一段325號","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
    {"name":"FlagPasta","address":"陽明街23巷5號","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
    {"name":"小食。候","address":"陽明街23巷13號","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
    {"name":"義匠義式湯麵","address":"陽明街32號","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
    {"name":"鄉親小吃","address":"幸福路16號","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
    {"name":"台南無刺虱目魚","address":"新海路97號","url":"https://maps.app.goo.gl/7b41uvR3Bimf2iGR6"},
    {"name":"逸麵鍋燒","address":"新海路101號","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
    {"name":"is pasta","address":"文化路一段321號2樓","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"},
    {"name":"吉飽早餐","address":"文化路一段311-19號","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
    {"name":"太極鰲車輪餅","address":"漢生西路128號","url":"https://maps.app.goo.gl/xYUnsWEWp4qL1Mg48"},
    {"name":"小松拉麵","address":"自由路33號","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"},
    {"name":"一京咖哩","address":"陽明街109號","url":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8"},
    {"name":"致理飯糰","address":"文化路一段311巷24號","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
    {"name":"吳二麻辣鴨血","address":"文化路一段311之6號","url":"https://maps.app.goo.gl/wTVnP3P1BeXfMweHA"},
    {"name":"吉野烤肉飯","address":"文化路一段311-15號","url":"https://maps.app.goo.gl/4NuMrst9S6LaLsAAA"},
    {"name":"MABO POKE","address":"文化路一段311之3號","url":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9"},
    {"name":"小陳滷社","address":"文化路一段311巷22號","url":"https://maps.app.goo.gl/1hxJG1hFFHHWA8c69"},
    {"name":"Café Wanderer","address":"陽明街27巷7號","url":"https://maps.app.goo.gl/fY6ryS1ZkMVXLkyC9"},
    {"name":"紅居館台菜","address":"漢生西路94號","url":"https://maps.app.goo.gl/pM2ksGeQ3Dw59zup6"},
    {"name":"津之芳生魚片","address":"漢生西路119巷6號","url":"https://maps.app.goo.gl/hXiBDGueUK27AxST8"},
    {"name":"達利早餐","address":"文化路一段313號","url":"https://maps.app.goo.gl/TbbU1AfAajVtXUfC9"},
    {"name":"海雲韓式料理","address":"自由路39號","url":"https://maps.app.goo.gl/gQbAeUjs4MwnYePi7"},
    {"name":"好盤美味廚房","address":"新海路32號","url":"https://maps.app.goo.gl/SEBGrxw7sHZ32nG5A"},
    {"name":"8弄5焗烤","address":"文化路一段311-5號","url":"https://maps.app.goo.gl/yqBECv3p6rzyzA2JA"},
    {"name":"好食堂","address":"幸福路18號","url":"https://maps.app.goo.gl/ZQF4CXHdrNP1iHjo7"},
    {"name":"Coffee HABU","address":"文化路一段270巷3弄24號","url":"https://maps.app.goo.gl/JMJGTMYU2qceEreY8"},
    {"name":"NU PASTA","address":"陽明街56號","url":"https://maps.app.goo.gl/DTTT1RdrE712kae49"},
    {"name":"solemio","address":"文化路一段435巷31弄11號","url":"https://maps.app.goo.gl/oeCcG6ULj7Kvk4TR6"},
    {"name":"光東养茶","address":"陽明街131號","url":"https://maps.app.goo.gl/beXqvzWQBnMnArr66"},
    {"name":"8鍋臭臭鍋","address":"漢生西路96號","url":"https://maps.app.goo.gl/wSo2NswqGA6ABAPR8"},
    {"name":"韓鼓韓式料理","address":"新海路11號","url":"https://maps.app.goo.gl/UmPfLfW57evBk1Yr8"},
    {"name":"川蜀麻辣食堂","address":"文化路一段419-6號","url":"https://maps.app.goo.gl/c3XvA3uxBmn2fpys6"},
    {"name":"文化小吃","address":"文化路一段283-2號","url":"https://maps.app.goo.gl/MWo9nxznJXp18xt47"},
    {"name":"三合苑炒飯","address":"自由路7號","url":"https://maps.app.goo.gl/D16ix8BY449ZkZwQ7"},
    {"name":"芳鄰美而美","address":"文化路一段311-13號","url":"https://maps.app.goo.gl/nSKzHtvDUMurWkdz9"},
    {"name":"麻丹辣火鍋","address":"漢生西路89巷2號","url":"https://maps.app.goo.gl/aM2oj5QoV2i7so3V7"},
    {"name":"健康主義","address":"文化路一段311-18號","url":"https://maps.app.goo.gl/wiaty6nqfMybNpMT9"},
    {"name":"一室","address":"文化路一段285巷1弄1號","url":"https://maps.app.goo.gl/n7u9Mkz7m46x9PtZ6"},
    {"name":"拉亞漢堡","address":"文化路一段313號","url":"https://maps.app.goo.gl/9yEH5ff46jh4zcCf8"},
    {"name":"呷覓早午餐","address":"陽明街23巷6弄15號","url":"https://maps.app.goo.gl/oPN3qTcsq5aMUJk78"},
    {"name":"德堡牛排","address":"陽明街17-1號","url":"https://maps.app.goo.gl/joCCpusVhvJPYkRWA"},
    {"name":"沐屋咖喱","address":"介壽街34號","url":"https://maps.app.goo.gl/wjbtJCArMgGbnLKZ7"},
    {"name":"山東寶麵食","address":"幸福路17號","url":"https://maps.app.goo.gl/ZKpyH4qKqAuFoKpy6"},
    {"name":"無骨鵝肉","address":"漢生西路103號","url":"https://maps.app.goo.gl/zJN1PyjPkDdmbnDT8"},
    {"name":"餵公子吃餅","address":"自由路2號","url":"https://maps.app.goo.gl/6tcLqDACL4A8wtcbA"},
    {"name":"霸子牛排","address":"文化路一段345號","url":"https://maps.app.goo.gl/4oLSG7m4w25Ehstm7"},
    {"name":"燒惑燒肉","address":"文化路一段323號","url":"https://maps.app.goo.gl/aCYeMUYW4VZUrj7G7"},
    {"name":"食尚川府","address":"文化路一段311-21號","url":"https://maps.app.goo.gl/rhr1HHaZAV6XBR1z7"},
    {"name":"晨間廚房","address":"文化路一段311-24號","url":"https://maps.app.goo.gl/o5Xa4dFAdgjGYqM28"},
    {"name":"牪嗑牛排","address":"新海路63號","url":"https://maps.app.goo.gl/p9bi26hNbEpsNeS39"},
    {"name":"龍一海南雞","address":"文化路一段311之8號","url":"https://maps.app.goo.gl/H7s3eem2CT8p4JNJ8"},
]


# =========================
# 📍 自動分路
# =========================
def get_road(addr):
    if "文化路" in addr:
        return "文化路一段"
    if "陽明街" in addr:
        return "陽明街"
    if "新海路" in addr:
        return "新海路"
    if "幸福路" in addr:
        return "幸福路"
    if "漢生西路" in addr:
        return "漢生西路"
    if "自由路" in addr:
        return "自由路"
    if "介壽" in addr:
        return "介壽街"
    return "其他"


# =========================
# LINE webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()

    if not body or "events" not in body:
        return "OK"

    event = body["events"][0]
    msg = event.get("message", {}).get("text", "")
    reply_token = event.get("replyToken")

    if not reply_token:
        return "OK"

    if msg == "美食轉盤":
        reply(reply_token, [{
            "type": "template",
            "altText": "會員功能",
            "template": {
                "type": "buttons",
                "title": "會員功能",
                "text": "請選擇",
                "actions": [
                    {"type": "uri","label":"我是會員","uri":"https://food-roulette-bot.onrender.com/roulette"},
                    {"type": "uri","label":"我不是會員","uri":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform"}
                ]
            }
        }])

    elif msg == "美食清單":
        reply(reply_token, [{
            "type":"uri",
            "altText":"美食清單",
            "uri":"https://food-roulette-bot.onrender.com/list"
        }])

    else:
        reply(reply_token, [{"type":"text","text":"收到：" + msg}])

    return "OK"


# =========================
# 🎡 轉盤（不動）
# =========================
@app.route("/roulette")
def roulette():
    names = [p["name"] for p in places]

    html = """
    <html><head><meta charset="utf-8"></head>
    <body style="text-align:center;font-family:Arial;background:#fff3e6;">
    <h2>🎡 美食轉盤</h2>
    <p id="r">點開始</p>
    <button onclick="spin()">開始</button>

    <script>
    const data = %s;
    function spin(){
        document.getElementById("r").innerText =
        "👉 " + data[Math.floor(Math.random()*data.length)];
    }
    </script>
    </body></html>
    """ % json.dumps(names, ensure_ascii=False)

    return render_template_string(html)


# =========================
# 📍 清單（新版：分路）
# =========================
@app.route("/list")
def list_page():

    grouped = defaultdict(list)
    for p in places:
        road = get_road(p["address"])
        grouped[road].append(p)

    html = """
    <html>
    <head>
    <meta charset="utf-8">
    <title>美食清單</title>
    <style>
    body{font-family:Arial;background:#f7f3ea;margin:0;}
    .wrap{padding:15px;}
    .block{background:white;margin:10px 0;padding:10px;border-radius:12px;}
    .item{padding:6px 0;border-bottom:1px solid #eee;}
    a{color:#ff5c5c;text-decoration:none;}
    </style>
    </head>
    <body>
    <div class="wrap">
    <h2>🍜 板橋美食清單（依路分區）</h2>
    """

    for road, items in grouped.items():
        html += f"<div class='block'><h3>📍 {road}</h3>"
        for p in items:
            html += f"""
            <div class="item">
                <b>{p['name']}</b><br>
                📌 {p['address']}<br>
                🔗 <a href="{p['url']}" target="_blank">Google Maps</a>
            </div>
            """
        html += "</div>"

    html += "</div></body></html>"

    return render_template_string(html)


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
