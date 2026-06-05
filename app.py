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


@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()

    try:
        event = body["events"][0]
        msg = event["message"]["text"]
        reply_token = event["replyToken"]

        if msg == "美食轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 美食轉盤"},
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

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
    font-family:Arial;
    background:#f7f3ea;
}

/* 🔥 改成 RWD 主容器 */
.container{
    display:flex;
    height:100vh;
}

/* 左側清單 */
#panel{
    width:340px;
    background:#fff8ee;
    padding:12px;
    overflow:auto;
}

/* 卡片 */
.card{
    background:linear-gradient(135deg,#fff,#fff7ee);
    margin:8px 0;
    padding:10px;
    border-radius:14px;
    box-shadow:0 3px 10px rgba(0,0,0,0.08);
}

/* 地圖 */
#map{
    flex:1;
    position:relative;
    background:#f1eadf;
}

/* 中心 */
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
}

/* 路 */
.roadV,.roadH{
    position:absolute;
    background:#cdb79e;
    opacity:0.4;
}
.roadV{width:6px;height:100%;left:50%;}
.roadH{height:6px;width:100%;top:50%;}

/* 店家點 */
.food{
    position:absolute;
    transform:translate(-50%,-50%);
    text-align:center;
}

.pin{
    width:12px;height:12px;
    border-radius:50%;
    border:2px solid white;
    margin:auto;
}

.label{
    font-size:10px;
    background:white;
    padding:2px 6px;
    border-radius:8px;
}

/* 顏色 */
.red{background:#ff6b6b;}
.green{background:#51cf66;}
.blue{background:#4dabf7;}
.brown{background:#d9a066;}


/* 🔥🔥手機版直接變上下 */
@media (max-width: 768px){

    .container{
        flex-direction:column;
    }

    #panel{
        width:100%;
        height:40vh;
    }

    #map{
        height:60vh;
    }
}
</style>

</head>

<body>

<div class="container">

<div id="panel">
<h3>🍜 致理美食清單</h3>
"""

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
"""

    for i, p in enumerate(places):

        if p["type"] in ["早餐"]:
            color="green"
        elif p["type"] in ["燒肉","台菜","韓式"]:
            color="red"
        elif p["type"] in ["咖啡","健康"]:
            color="blue"
        else:
            color="brown"

        top = 20 + (i % 6) * 10
        left = 20 + (i % 5) * 15

        html += f"""
        <div class="food {color}" style="top:{top}%;left:{left}%;">
            <div class="pin"></div>
            <div class="label">{p['name']}</div>
        </div>
        """

    html += """
</div>

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
