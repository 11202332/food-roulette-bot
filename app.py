from flask import Flask, request, render_template_string
import requests
import os
import json

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
# 🍜 店家資料
# =========================
places = [
    {"name":"栄次郎個人燒肉","area":"文化路","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
    {"name":"FlagPasta","area":"陽明街","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
    {"name":"小食。候","area":"陽明街","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
    {"name":"義匠義式湯麵","area":"陽明街","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
    {"name":"鄉親小吃","area":"幸福路","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
    {"name":"台南無刺虱目魚","area":"新海路","url":"https://maps.app.goo.gl/7b41uvR3Bimf2iGR8"},
    {"name":"逸麵鍋燒","area":"新海路","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
    {"name":"is pasta","area":"文化路","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"},
    {"name":"吉飽早餐","area":"文化路","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
    {"name":"太極鰲車輪餅","area":"漢生西路","url":"https://maps.app.goo.gl/xYUnsWEWp4qL1Mg48"},
    {"name":"小松拉麵","area":"陽明街","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"},
    {"name":"一京咖哩","area":"陽明街","url":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8"},
    {"name":"致理飯糰","area":"文化路","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
    {"name":"吳二麻辣鴨血","area":"文化路","url":"https://maps.app.goo.gl/wTVnP3P1BeXfMweHA"},
    {"name":"吉野烤肉飯","area":"文化路","url":"https://maps.app.goo.gl/4NuMrst9S6LaLsAAA"},
    {"name":"MABO POKE","area":"文化路","url":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9"},
    {"name":"小陳滷社","area":"文化路","url":"https://maps.app.goo.gl/1hxJG1hFFHHWA8c69"},
    {"name":"Café Wanderer","area":"陽明街","url":"https://maps.app.goo.gl/fY6ryS1ZkMVXLkyC9"},
    {"name":"紅居館","area":"漢生西路","url":"https://maps.app.goo.gl/pM2ksGeQ3Dw59zup6"},
    {"name":"津之芳","area":"漢生西路","url":"https://maps.app.goo.gl/hXiBDGueUK27AxST8"},
    {"name":"海雲韓式料理","area":"自由路","url":"https://maps.app.goo.gl/gQbAeUjs4MwnYePi7"},
    {"name":"NU PASTA","area":"陽明街","url":"https://maps.app.goo.gl/DTTT1RdrE712kae49"},
    {"name":"solemio","area":"文化路","url":"https://maps.app.goo.gl/oeCcG6ULj7Kvk4TR6"},
    {"name":"光東养茶","area":"陽明街","url":"https://maps.app.goo.gl/beXqvzWQBnMnArr66"},
    {"name":"8鍋臭臭鍋","area":"漢生西路","url":"https://maps.app.goo.gl/wSo2NswqGA6ABAPR8"},
    {"name":"韓鼓韓式料理","area":"新海路","url":"https://maps.app.goo.gl/UmPfLfW57evBk1Yr8"},
    {"name":"川蜀麻辣食堂","area":"文化路","url":"https://maps.app.goo.gl/c3XvA3uxBmn2fpys6"},
    {"name":"文化小吃","area":"文化路","url":"https://maps.app.goo.gl/MWo9nxznJXp18xt47"},
    {"name":"三合苑炒飯","area":"自由路","url":"https://maps.app.goo.gl/D16ix8BY449ZkZwQ7"},
    {"name":"芳鄰美而美","area":"文化路","url":"https://maps.app.goo.gl/nSKzHtvDUMurWkdz9"},
    {"name":"麻丹辣火鍋","area":"漢生西路","url":"https://maps.app.goo.gl/aM2oj5QoV2i7so3V7"},
    {"name":"健康主義","area":"文化路","url":"https://maps.app.goo.gl/wiaty6nqfMybNpMT9"},
    {"name":"一室","area":"文化路","url":"https://maps.app.goo.gl/n7u9Mkz7m46x9PtZ6"},
    {"name":"拉亞漢堡","area":"文化路","url":"https://maps.app.goo.gl/9yEH5ff46jh4zcCf8"},
    {"name":"呷覓早午餐","area":"陽明街","url":"https://maps.app.goo.gl/oPN3qTcsq5aMUJk78"},
    {"name":"德堡牛排","area":"陽明街","url":"https://maps.app.goo.gl/joCCpusVhvJPYkRWA"},
    {"name":"沐屋咖喱","area":"介壽街","url":"https://maps.app.goo.gl/wjbtJCArMgGbnLKZ7"},
    {"name":"山東寶麵食館","area":"幸福路","url":"https://maps.app.goo.gl/ZKpyH4qKqAuFoKpy6"},
    {"name":"無骨鵝肉","area":"漢生西路","url":"https://maps.app.goo.gl/zJN1PyjPkDdmbnDT8"},
    {"name":"餵公子吃餅","area":"自由路","url":"https://maps.app.goo.gl/6tcLqDACL4A8wtcbA"},
    {"name":"霸子牛排","area":"文化路","url":"https://maps.app.goo.gl/4oLSG7m4w25Ehstm7"},
    {"name":"燒惑燒肉","area":"文化路","url":"https://maps.app.goo.gl/aCYeMUYW4VZUrj7G7"},
    {"name":"食尚川府","area":"文化路","url":"https://maps.app.goo.gl/rhr1HHaZAV6XBR1z7"},
    {"name":"晨間廚房","area":"文化路","url":"https://maps.app.goo.gl/o5Xa4dFAdgjGYqM28"},
    {"name":"牪嗑牛排","area":"新海路","url":"https://maps.app.goo.gl/p9bi26hNbEpsNeS39"},
    {"name":"龍一海南雞","area":"文化路","url":"https://maps.app.goo.gl/H7s3eem2CT8p4JNJ8"}
]


# =========================
# LINE webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()
    if not body:
        return "OK"

    event = body["events"][0]

    if "message" not in event:
        return "OK"

    msg = event["message"].get("text", "")
    reply_token = event.get("replyToken")

    if not reply_token:
        return "OK"

    # 🎡 轉盤（完全原版，不改）
    if msg == "美食轉盤":
        reply(reply_token, [{
            "type": "template",
            "altText": "會員功能",
            "template": {
                "type": "buttons",
                "title": "美食轉盤",
                "text": "選擇功能",
                "actions": [
                    {
                        "type": "uri",
                        "label": "我是會員",
                        "uri": "https://food-roulette-bot.onrender.com/roulette"
                    },
                    {
                        "type": "uri",
                        "label": "我不是會員",
                        "uri": "https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform?usp=header"
                    }
                ]
            }
        }])

    # 🍜 地圖 → 清單（已移除 map 頁面）
    elif msg == "美食地圖":

        grouped = {}
        for p in places:
            grouped.setdefault(p["area"], []).append(p)

        text = "🍜 致理美食清單\n\n"

        for area, items in grouped.items():
            text += f"📍 {area}\n"
            for i in items:
                text += f"- {i['name']}\n{i['url']}\n"
            text += "\n"

        reply(reply_token, [{"type":"text","text":text}])

    else:
        reply(reply_token, [{"type":"text","text":"收到：" + msg}])


    return "OK"


# =========================
# 🎡 轉盤（原版）
# =========================
@app.route("/roulette")
def roulette():

    names = [p["name"] for p in places]

    html = """
    <html>
    <head>
    <meta charset="utf-8">
    <title>轉盤</title>
    </head>

    <body style="text-align:center;font-family:Arial;background:#fff3e6;">

        <h2>🎡 美食轉盤</h2>

        <p id="result">點擊開始</p>

        <button onclick="spin()">開始</button>

        <script>
        const places = %s;

        function spin(){
            const pick = places[Math.floor(Math.random()*places.length)];
            document.getElementById("result").innerText = "👉 " + pick;
        }
        </script>

    </body>
    </html>
    """ % json.dumps(names, ensure_ascii=False)

    return render_template_string(html)


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
