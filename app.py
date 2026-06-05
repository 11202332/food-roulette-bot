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
# 🍜 店家資料（完整）
# =========================
places = [
{"name":"栄次郎個人燒肉","road":"文化路","rating":4.7,"price":"$200-400","comment":"燒肉"},
{"name":"FlagPasta","road":"陽明街","rating":4.5,"price":"$200-400","comment":"義大利麵"},
{"name":"小食。候","road":"陽明街","rating":4.3,"price":"$200-400","comment":"咖啡"},
{"name":"義匠義式湯麵","road":"陽明街","rating":4.8,"price":"$200-400","comment":"湯麵"},
{"name":"鄉親小吃","road":"幸福路","rating":4.6,"price":"$1-200","comment":"小吃"},
{"name":"逸麵鍋燒","road":"新海路","rating":4.9,"price":"$1-200","comment":"鍋燒"},
{"name":"is pasta","road":"文化路","rating":4.3,"price":"$200-400","comment":"義大利麵"},
{"name":"吉飽早餐","road":"文化路","rating":4.0,"price":"$1-200","comment":"早餐"},
{"name":"致理飯糰","road":"文化路","rating":4.7,"price":"$1-200","comment":"早餐"},
{"name":"小松拉麵","road":"陽明街","rating":4.5,"price":"$1-200","comment":"拉麵"},
{"name":"一京咖哩","road":"陽明街","rating":4.6,"price":"$1-200","comment":"咖哩"},
{"name":"吳二麻辣鴨血","road":"文化路","rating":4.4,"price":"$1-200","comment":"麻辣"},
{"name":"吉野烤肉飯","road":"文化路","rating":3.8,"price":"$1-200","comment":"便當"},
{"name":"MABO POKE","road":"文化路","rating":4.3,"price":"$1-200","comment":"健康"},
{"name":"Café Wanderer","road":"陽明街","rating":4.4,"price":"$200-400","comment":"咖啡"},
{"name":"紅居館台菜","road":"漢生西路","rating":4.8,"price":"$400-800","comment":"台菜"},
{"name":"海雲韓式料理","road":"自由路","rating":4.7,"price":"$400-600","comment":"韓式"},
{"name":"NU PASTA","road":"陽明街","rating":4.6,"price":"$200-400","comment":"義大利麵"},
{"name":"光東養茶","road":"陽明街","rating":4.7,"price":"$1-200","comment":"飲料"},
{"name":"8鍋臭臭鍋","road":"漢生西路","rating":3.9,"price":"$1-200","comment":"火鍋"},
{"name":"麻丹辣小火鍋","road":"漢生西路","rating":4.9,"price":"$200-400","comment":"火鍋"},
{"name":"牪嗑牛排","road":"新海路","rating":4.3,"price":"$200-400","comment":"牛排"},
{"name":"龍一海南雞","road":"文化路","rating":4.6,"price":"$1-200","comment":"便當"},
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

        # 🎡 轉盤（完全保留你的版本）
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
                {"type":"text","text":"📝 會員表單"},
                {"type":"text","text":"https://forms.gle/jYykimjWcX1rgYRW8"}
            ])

        # 🗺️ 美食地圖（純清單，不再有地圖）
        elif msg == "美食地圖":

            grouped = {}
            for p in places:
                grouped.setdefault(p["road"], []).append(p)

            text = "🍜 致理美食清單\n\n"

            for road, items in grouped.items():
                text += f"📍 {road}\n"
                for i in items:
                    text += f"- {i['name']} ⭐{i['rating']} {i['price']}\n"
                text += "\n"

            reply(reply_token, [{"type":"text","text":text}])

        else:
            reply(reply_token, [{"type":"text","text":"收到：" + msg}])

        return "OK"

    except Exception as e:
        print("error:", e)
        return "OK"


# =========================
# home
# =========================
@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
