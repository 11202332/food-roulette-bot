from flask import Flask, request, render_template_string
import requests
import os
import json
import random

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
# 🍜 50家店（簡化資料）
# =========================

places = [
{"name":"栄次郎個人燒肉","rating":4.7,"price":"$200-400","type":"燒肉","comment":"自己烤肉很爽但錢包會痛"},
{"name":"FlagPasta","rating":4.5,"price":"$200-400","type":"義大利麵","comment":"穩定不踩雷"},
{"name":"小食。候","rating":4.3,"price":"$200-400","type":"咖啡","comment":"安靜但容易客滿"},
{"name":"義匠義式湯麵","rating":4.8,"price":"$200-400","type":"義大利麵","comment":"濃郁湯麵很特別"},
{"name":"鄉親小吃","rating":4.6,"price":"$1-200","type":"小吃","comment":"便宜實在"},
{"name":"台南無刺虱目魚","rating":4.4,"price":"$1-200","type":"小吃","comment":"清爽魚湯"},
{"name":"逸麵鍋燒","rating":4.9,"price":"$1-200","type":"鍋燒","comment":"湯頭超強"},
{"name":"is pasta","rating":4.3,"price":"$200-400","type":"義大利麵","comment":"學生聚餐常去"},
{"name":"吉飽早餐","rating":4.0,"price":"$1-200","type":"早餐","comment":"早八救星"},
{"name":"太極鰲車輪餅","rating":4.3,"price":"$1-200","type":"點心","comment":"下午茶很讚"},
{"name":"小松拉麵","rating":4.5,"price":"$1-200","type":"日式","comment":"平價拉麵"},
{"name":"一京咖哩","rating":4.6,"price":"$1-200","type":"咖哩","comment":"咖哩濃郁"},
{"name":"致理飯糰","rating":4.7,"price":"$1-200","type":"早餐","comment":"飯糰超大顆"},
{"name":"吳二麻辣鴨血","rating":4.4,"price":"$1-200","type":"麻辣","comment":"冬天必吃"},
{"name":"吉野烤肉飯","rating":3.8,"price":"$1-200","type":"便當","comment":"快速解決"},
{"name":"MABO POKE","rating":4.3,"price":"$1-200","type":"健康","comment":"清爽路線"},
{"name":"小陳滷社","rating":3.9,"price":"$1-200","type":"滷味","comment":"宵夜用"},
{"name":"Café Wanderer","rating":4.4,"price":"$200-400","type":"咖啡","comment":"文青咖啡廳"},
{"name":"紅居館台菜","rating":4.8,"price":"$400-800","type":"台菜","comment":"聚餐用"},
{"name":"津之芳生魚片","rating":4.2,"price":"$200-400","type":"日式","comment":"海鮮新鮮"},
{"name":"達利早餐","rating":3.9,"price":"$1-200","type":"早餐","comment":"普通早餐店"},
{"name":"海雲韓式料理","rating":4.7,"price":"$400-600","type":"韓式","comment":"炸雞好吃"},
{"name":"好食堂","rating":4.2,"price":"$1-200","type":"便當","comment":"份量大"},
{"name":"NU PASTA","rating":4.6,"price":"$200-400","type":"義大利麵","comment":"穩定聚餐"},
{"name":"solemio","rating":4.4,"price":"$200-400","type":"義大利麵","comment":"環境好"},
{"name":"光東養茶","rating":4.7,"price":"$1-200","type":"飲料","comment":"茶味乾淨"},
{"name":"8鍋臭臭鍋","rating":3.9,"price":"$1-200","type":"火鍋","comment":"平價火鍋"},
{"name":"韓鼓韓式料理","rating":4.3,"price":"$400-600","type":"韓式","comment":"聚餐用"},
{"name":"川蜀麻辣食堂","rating":4.3,"price":"$200-400","type":"麻辣","comment":"重口味"},
{"name":"文化小吃","rating":3.9,"price":"$1-200","type":"小吃","comment":"月底救星"},
{"name":"芳鄰美而美","rating":4.0,"price":"$1-200","type":"早餐","comment":"傳統早餐"},
{"name":"麻丹辣小火鍋","rating":4.9,"price":"$200-400","type":"火鍋","comment":"學生最愛"},
{"name":"健康主義","rating":4.2,"price":"$200-400","type":"健康","comment":"清爽便當"},
{"name":"一室","rating":4.8,"price":"$1-200","type":"咖啡","comment":"安靜空間"},
{"name":"拉亞漢堡","rating":3.8,"price":"$1-200","type":"早餐","comment":"連鎖早餐"},
{"name":"呷覓早午餐","rating":4.8,"price":"$1-200","type":"早餐","comment":"外帶方便"},
{"name":"德堡牛排","rating":4.0,"price":"$200-400","type":"牛排","comment":"平價牛排"},
{"name":"沐屋咖喱","rating":4.6,"price":"$1-200","type":"咖哩","comment":"日式咖哩"},
{"name":"山東寶麵食館","rating":4.4,"price":"$1-200","type":"麵食","comment":"份量大"},
{"name":"無骨鵝肉","rating":4.2,"price":"$1-200","type":"小吃","comment":"鵝肉好吃"},
{"name":"餵公子吃餅","rating":4.7,"price":"$1-200","type":"點心","comment":"甜點店"},
{"name":"霸子牛排","rating":4.0,"price":"$400-600","type":"牛排","comment":"西餐牛排"},
{"name":"燒惑日式燒肉","rating":4.4,"price":"$400-600","type":"燒肉","comment":"聚餐燒肉"},
{"name":"食尚川府","rating":4.8,"price":"$1-200","type":"川菜","comment":"麻辣好吃"},
{"name":"晨間廚房","rating":3.1,"price":"$1-200","type":"早餐","comment":"普通早餐"},
{"name":"牪嗑牛排","rating":4.3,"price":"$200-400","type":"牛排","comment":"學生牛排"},
{"name":"龍一海南雞","rating":4.6,"price":"$1-200","type":"便當","comment":"雞肉很嫩"},
]



# =========================
# webhook（LINE）
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
                {"type":"text","text":"📝 填寫會員"},
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
# 🌍 手繪地圖（簡化版）
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

#panel{
    width:320px;
    background:#fafafa;
    padding:10px;
    overflow:auto;
}

.card{
    background:white;
    margin:8px 0;
    padding:10px;
    border-radius:12px;
    border:1px solid #eee;
}

#map{
    flex:1;
    position:relative;
    background:#f2efe9;
}

.center{
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    background:#ff6b6b;
    color:white;
    padding:6px 12px;
    border-radius:20px;
    font-size:12px;
}

.dot{
    position:absolute;
    width:10px;
    height:10px;
    background:#333;
    border-radius:50%;
}

.zone{
    position:absolute;
    font-size:12px;
    color:#666;
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
            {p['desc']}
        </div>
        """

    html += """
</div>

<div id="map">

<div class="center">致理科大</div>

<div class="zone" style="top:10%;left:60%;">文化路</div>
<div class="zone" style="top:40%;left:65%;">陽明街</div>
<div class="zone" style="top:70%;left:55%;">新海路</div>
"""

    # 隨機分散點
    for p in places:
        top = random.randint(10, 85)
        left = random.randint(45, 90)

        html += f"""
        <div class="dot" style="top:{top}%;left:{left}%;" title="{p['name']}"></div>
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
