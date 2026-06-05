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
# 店家資料
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
# LINE webhook（會員判斷）
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()

    try:
        event = body["events"][0]
        msg = event["message"]["text"]
        reply_token = event["replyToken"]

        # 🎡 美食轉盤 → 會員判斷
        if msg == "美食轉盤":
            reply(reply_token, [{
                "type":"template",
                "altText":"會員驗證",
                "template":{
                    "type":"buttons",
                    "text":"你是會員嗎？",
                    "actions":[
                        {
                            "type":"uri",
                            "label":"我是會員（開轉盤）",
                            "uri":"https://cute-melomakarona-859d27.netlify.app"
                        },
                        {
                            "type":"uri",
                            "label":"我不是會員（填表單）",
                            "uri":"https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform?usp=header"
                        }
                    ]
                }
            }])

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
