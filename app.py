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
# 🍜 店家資料（完整含 Google Maps）
# =========================
places = [
    {"name":"栄次郎個人燒肉—板橋文化店","address":"220新北市板橋區忠誠里文化路一段325號","rating":"4.7","price":"$200-400","time":"11:30-23:30","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
    {"name":"FlagPasta","address":"220新北市板橋區忠誠里陽明街23巷5號","rating":"4.5","price":"$200-400","time":"11:00-21:00","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
    {"name":"小食。候","address":"220新北市板橋區忠誠里陽明街23巷13號1樓","rating":"4.3","price":"$200-400","time":"12:00-19:00","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
    {"name":"義匠義式湯麵-板橋陽明店","address":"220新北市板橋區陽明街32號","rating":"4.8","price":"$200-400","time":"11:30-21:00","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
    {"name":"鄉親小吃","address":"220新北市板橋區公舘里幸福路16號","rating":"4.6","price":"","time":"11:00-19:00","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},

    {"name":"台南無刺虱目魚系列專賣店","address":"220新北市板橋區幸福里新海路97號","rating":"4.4","price":"$1-200","time":"11:00-22:00","url":"https://maps.app.goo.gl/7b41uvR3Bimf2iGR8"},
    {"name":"逸麵麵鍋燒專賣","address":"220新北市板橋區幸福里新海路101號","rating":"4.9","price":"$1-200","time":"11:30-21:00","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
    {"name":"is pasta 義大利麵","address":"220新北市板橋區文化路一段321號2樓","rating":"4.3","price":"$200-400","time":"11:20-21:15","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"},
    {"name":"吉飽早餐-致理店","address":"220新北市板橋區文化路一段311-19號","rating":"4.0","price":"$1-200","time":"7:00-14:00","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
    {"name":"太極鰲車輪餅","address":"220新北市板橋區漢生西路128號","rating":"4.3","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/xYUnsWEWp4qL1Mg48"},

    {"name":"小松拉麵","address":"220新北市板橋區自由路33號","rating":"4.5","price":"$1-200","time":"11:30-21:30","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"},
    {"name":"一京咖哩","address":"220新北市板橋區陽明街109號","rating":"4.6","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8"},
    {"name":"致理飯糰","address":"220新北市板橋區文化路一段311巷24號","rating":"4.7","price":"$1-200","time":"9:00-17:15","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
    {"name":"吳二麻辣鴨血","address":"220新北市板橋區文化路一段311之6號","rating":"4.4","price":"$1-200","time":"10:30-20:30","url":"https://maps.app.goo.gl/wTVnP3P1BeXfMweHA"},
    {"name":"吉野烤肉飯","address":"220新北市板橋區文化路一段311-15號","rating":"3.8","price":"$1-200","time":"10:30-20:00","url":"https://maps.app.goo.gl/4NuMrst9S6LaLsAAA"},

    {"name":"MABO POKE","address":"220新北市板橋區文化路一段311之3號","rating":"4.3","price":"$1-200","time":"11:00-20:30","url":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9"},
    {"name":"小陳滷社","address":"220新北市板橋區文化路一段311巷22號","rating":"3.9","price":"$1-200","time":"11:30-20:00","url":"https://maps.app.goo.gl/1hxJG1hFFHHWA8c69"},
    {"name":"Café Wanderer","address":"220新北市板橋區陽明街27巷7號","rating":"4.4","price":"$200-400","time":"10:00-20:30","url":"https://maps.app.goo.gl/fY6ryS1ZkMVXLkyC9"},
    {"name":"紅居館","address":"220新北市板橋區漢生西路94號","rating":"4.8","price":"$400-800","time":"17:00-23:30","url":"https://maps.app.goo.gl/pM2ksGeQ3Dw59zup6"},
    {"name":"津之芳生魚片","address":"220新北市板橋區漢生西路119巷6號","rating":"4.2","price":"$200-400","time":"11:00-20:30","url":"https://maps.app.goo.gl/hXiBDGueUK27AxST8"},

    {"name":"達利早餐","address":"220新北市板橋區文化路一段313號","rating":"3.9","price":"$1-200","time":"7:00-15:00","url":"https://maps.app.goo.gl/TbbU1AfAajVtXUfC9"},
    {"name":"海雲韓式料理","address":"220新北市板橋區自由路39號","rating":"4.7","price":"$400-600","time":"11:00-21:00","url":"https://maps.app.goo.gl/gQbAeUjs4MwnYePi7"},
    {"name":"好盤美味廚房","address":"220新北市板橋區新海路32號","rating":"4.3","price":"$200-400","time":"11:00-21:30","url":"https://maps.app.goo.gl/SEBGrxw7sHZ32nG5A"},
    {"name":"8弄5焗烤廚房","address":"220新北市板橋區文化路一段311-5號","rating":"3.6","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/yqBECv3p6rzyzA2JA"},
    {"name":"好食堂","address":"220新北市板橋區幸福路18號","rating":"4.2","price":"$1-200","time":"11:30-20:00","url":"https://maps.app.goo.gl/ZQF4CXHdrNP1iHjo7"},

    {"name":"Coffee HABU","address":"220新北市板橋區文化路一段270巷3弄24號","rating":"4.8","price":"$200-400","time":"11:00-20:00","url":"https://maps.app.goo.gl/JMJGTMYU2qceEreY8"},
    {"name":"NU PASTA","address":"220新北市板橋區陽明街56號58號","rating":"4.6","price":"$200-400","time":"11:00-21:00","url":"https://maps.app.goo.gl/DTTT1RdrE712kae49"},
    {"name":"solemio","address":"220新北市板橋區文化路一段435巷31弄11號","rating":"4.4","price":"$200-400","time":"11:00-21:15","url":"https://maps.app.goo.gl/oeCcG6ULj7Kvk4TR6"},
    {"name":"光東养茶","address":"220新北市板橋區陽明街131號","rating":"4.7","price":"$1-200","time":"10:30-20:30","url":"https://maps.app.goo.gl/beXqvzWQBnMnArr66"},
    {"name":"8鍋臭臭鍋","address":"220新北市板橋區漢生西路96號","rating":"3.9","price":"$1-200","time":"11:30-23:00","url":"https://maps.app.goo.gl/wSo2NswqGA6ABAPR8"},

    {"name":"韓鼓韓式料理","address":"220新北市板橋區新海路11號","rating":"4.3","price":"$400-600","time":"11:30-21:00","url":"https://maps.app.goo.gl/UmPfLfW57evBk1Yr8"},
    {"name":"川蜀麻辣食堂","address":"220新北市板橋區文化路一段419-6號","rating":"4.3","price":"$200-400","time":"11:00-22:00","url":"https://maps.app.goo.gl/c3XvA3uxBmn2fpys6"},
    {"name":"文化小吃","address":"220新北市板橋區文化路一段283-2號","rating":"3.9","price":"$1-200","time":"11:00-20:30","url":"https://maps.app.goo.gl/MWo9nxznJXp18xt47"},
    {"name":"三合苑炒飯炒麵","address":"220新北市板橋區自由路7號","rating":"4.3","price":"$1-200","time":"11:00-21:00","url":"https://maps.app.goo.gl/D16ix8BY449ZkZwQ7"},
    {"name":"芳鄰美而美","address":"220新北市板橋區文化路一段311-13號","rating":"4.0","price":"$1-200","time":"6:00-14:00","url":"https://maps.app.goo.gl/nSKzHtvDUMurWkdz9"},

    {"name":"麻丹辣小火鍋","address":"220新北市板橋區漢生西路89巷2號","rating":"4.9","price":"$200-400","time":"11:30-21:00","url":"https://maps.app.goo.gl/aM2oj5QoV2i7so3V7"},
    {"name":"健康主義","address":"220新北市板橋區文化路一段311-18號","rating":"4.2","price":"$200-400","time":"6:00-15:00","url":"https://maps.app.goo.gl/wiaty6nqfMybNpMT9"},
    {"name":"一室","address":"220新北市板橋區文化路一段285巷1弄1號","rating":"4.8","price":"$1-200","time":"12:00-19:30","url":"https://maps.app.goo.gl/n7u9Mkz7m46x9PtZ6"},
    {"name":"拉亞漢堡","address":"220新北市板橋區文化路一段313號","rating":"3.8","price":"$1-200","time":"6:00-14:00","url":"https://maps.app.goo.gl/9yEH5ff46jh4zcCf8"},
    {"name":"呷覓早午餐","address":"220新北市板橋區陽明街23巷6弄15號","rating":"4.8","price":"$1-200","time":"7:00-18:00","url":"https://maps.app.goo.gl/oPN3qTcsq5aMUJk78"},

    {"name":"德堡牛排","address":"220新北市板橋區陽明街17-1號","rating":"4.0","price":"$200-400","time":"11:30-21:30","url":"https://maps.app.goo.gl/joCCpusVhvJPYkRWA"},
    {"name":"沐屋咖喱","address":"220新北市板橋區介壽街34號","rating":"4.6","price":"$1-200","time":"11:00-14:00","url":"https://maps.app.goo.gl/wjbtJCArMgGbnLKZ7"},
    {"name":"山東寶麵食館","address":"220新北市板橋區幸福路17號","rating":"4.4","price":"$1-200","time":"11:30-21:00","url":"https://maps.app.goo.gl/ZKpyH4qKqAuFoKpy6"},
    {"name":"無骨鵝肉","address":"220新北市板橋區漢生西路103號","rating":"4.2","price":"$1-200","time":"11:30-20:30","url":"https://maps.app.goo.gl/zJN1PyjPkDdmbnDT3"},
    {"name":"餵公子吃餅","address":"220新北市板橋區自由路2號","rating":"4.7","price":"$1-200","time":"14:00-18:00","url":"https://maps.app.goo.gl/6tcLqDACL4A8wtcbA"},

    {"name":"霸子牛排","address":"220新北市板橋區文化路一段345號","rating":"4.0","price":"$400-600","time":"11:00-21:30","url":"https://maps.app.goo.gl/4oLSG7m4w25Ehstm7"},
    {"name":"燒惑日式燒肉","address":"220新北市板橋區文化路一段323號","rating":"4.4","price":"$400-600","time":"12:00-22:30","url":"https://maps.app.goo.gl/aCYeMUYW4VZUrj7G7"},
    {"name":"食尚川府","address":"220新北市板橋區文化路一段311-21號","rating":"4.8","price":"$1-200","time":"11:00-20:00","url":"https://maps.app.goo.gl/rhr1HHaZAV6XBR1z7"},
    {"name":"晨間廚房","address":"220新北市板橋區文化路一段311-24號","rating":"3.1","price":"$1-200","time":"7:00-14:30","url":"https://maps.app.goo.gl/o5Xa4dFAdgjGYqM28"},
    {"name":"牪嗑牛排","address":"220新北市板橋區新海路63號","rating":"4.3","price":"$200-400","time":"11:30-22:00","url":"https://maps.app.goo.gl/p9bi26hNbEpsNeS39"},

    {"name":"龍一海南雞","address":"220新北市板橋區文化路一段311之8號","rating":"4.6","price":"$1-200","time":"10:30-19:00","url":"https://maps.app.goo.gl/H7s3eem2CT8p4JNJ8"}
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

        # 🎡 轉盤（會員）
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
                            {"type":"uri","label":"我不是會員",
                             "uri":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform?usp=header"}
                        ]
                    }
                }
            ])

        elif msg == "進入轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 轉盤開啟"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
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
# 🗺️ 地圖（完整可點 Google Maps）
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
    font-family:Arial;
    display:flex;
    height:100vh;
}

#panel{
    width:380px;
    background:#fff8ee;
    padding:12px;
    overflow:auto;
}

.card{
    background:white;
    margin:10px 0;
    padding:12px;
    border-radius:14px;
    box-shadow:0 2px 6px rgba(0,0,0,0.1);
}

.name{
    font-size:16px;
    font-weight:bold;
}

a{
    display:inline-block;
    margin-top:8px;
    background:#ff4d4d;
    color:white;
    padding:6px 10px;
    border-radius:8px;
    text-decoration:none;
}
</style>
</head>

<body>

<div id="panel">
<h2>🍜 致理美食清單</h2>
"""

    for p in places:
        html += f"""
        <div class="card">
            <div class="name">{p['name']}</div>
            ⭐ {p['rating']} | {p['price']}<br>
            {p['comment']}<br>

            <a href="{p['map']}" target="_blank">📍 開啟 Google Maps</a>
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
