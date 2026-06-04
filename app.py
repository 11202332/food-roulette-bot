from flask import Flask, request
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
    requests.post(
        LINE_API,
        headers=headers,
        data=json.dumps({"replyToken": reply_token, "messages": messages})
    )


# =========================
# 📌 80家店（先給你架構＋示範）
# 👉 你之後可以一直往下加
# =========================
places = [
    # ===== 台式 =====
    {"name":"致理飯糰","address":"板橋文化路一段","type":"台式","rating":4.3,"reviews":120,"hours":"06:30–10:30"},
    {"name":"小陳滷味","address":"板橋文化路一段","type":"台式","rating":4.5,"reviews":210,"hours":"17:00–23:30"},
    {"name":"阿房滷味","address":"板橋文化路一段","type":"台式","rating":4.2,"reviews":180,"hours":"16:30–23:00"},
    {"name":"大碗公當歸羊肉","address":"板橋文化路一段","type":"台式","rating":4.4,"reviews":95,"hours":"11:00–22:00"},
    {"name":"油庫口麵線","address":"板橋文化路一段","type":"台式","rating":4.6,"reviews":3000,"hours":"09:00–18:00"},

    # ===== 早午餐 =====
    {"name":"麥味登致理店","address":"板橋文化路一段","type":"早午餐","rating":4.0,"reviews":260,"hours":"06:00–13:30"},
    {"name":"麥當勞文化店","address":"板橋文化路一段","type":"早午餐","rating":4.2,"reviews":980,"hours":"24小時"},
    {"name":"晨間廚房","address":"板橋文化路一段","type":"早午餐","rating":4.1,"reviews":340,"hours":"06:00–14:00"},

    # ===== 日式義式 =====
    {"name":"薩莉亞","address":"板橋文化路一段","type":"日式義式","rating":4.1,"reviews":530,"hours":"11:00–22:00"},
    {"name":"Sukiya","address":"板橋文化路一段","type":"日式義式","rating":4.4,"reviews":410,"hours":"24小時"},
    {"name":"Is Pasta","address":"板橋文化路一段","type":"日式義式","rating":4.3,"reviews":210,"hours":"11:00–21:30"},

    # ===== 咖啡 =====
    {"name":"路易莎","address":"板橋文化路一段","type":"咖啡","rating":4.4,"reviews":620,"hours":"07:00–21:00"},
    {"name":"星巴克","address":"板橋文化路一段","type":"咖啡","rating":4.5,"reviews":890,"hours":"07:00–22:00"},

    # ===== 宵夜 =====
    {"name":"微笑炭烤","address":"板橋文化路一段","type":"宵夜","rating":4.3,"reviews":150,"hours":"18:00–01:00"},
    {"name":"阿耀臭豆腐","address":"板橋文化路一段","type":"宵夜","rating":4.2,"reviews":180,"hours":"17:00–00:30"},
]

# 👉 讓你快速擴充到 80 家（關鍵）
# 你之後只要一直 append 就好


# =========================
# 🎡 轉盤功能（真正隨機）
# =========================
def spin_food():
    return random.choice(places)


# =========================
# LINE webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()

    try:
        event = body["events"][0]

        if "message" not in event:
            return "OK"

        if event["message"]["type"] != "text":
            return "OK"

        reply_token = event["replyToken"]
        msg = event["message"]["text"]

        # =========================
        # 🎡 美食轉盤（重點升級）
        # =========================
        if msg == "美食轉盤":

            reply(reply_token, [
                {"type":"text","text":"🎡 美食轉盤啟動中..."},
                {
                    "type": "text",
                    "text": "👉 點擊「我是會員」開始抽店"
                }
            ])

        elif msg == "進入轉盤":

            food = spin_food()

            maps_url = f"https://www.google.com/maps/search/?api=1&query={food['name']} {food['address']}"

            reply(reply_token, [
                {
                    "type": "text",
                    "text":
f"""🎯 幫你抽到了！

🍜 {food['name']}
📍 {food['address']}
⭐ {food['rating']}（{food['reviews']}）
🕒 {food['hours']}"""
                },
                {
                    "type": "text",
                    "text": maps_url
                }
            ])

        elif msg == "加入會員":

            reply(reply_token, [
                {"type":"text","text":"📝 請填寫會員表單"},
                {"type":"text","text":"https://forms.gle/jYykimjWcX1rgYRW8"}
            ])

        # =========================
        # 🗺️ 地圖入口
        # =========================
        elif msg == "美食地圖":

            reply(reply_token, [{
                "type": "template",
                "altText": "美食地圖",
                "template": {
                    "type": "buttons",
                    "text": "🍜 致理周邊美食地圖",
                    "actions": [
                        {
                            "type": "uri",
                            "label": "打開地圖",
                            "uri": "https://food-roulette-bot.onrender.com/map"
                        }
                    ]
                }
            }])

        else:

            reply(reply_token, [
                {"type":"text","text":"收到：" + msg}
            ])

        return "OK"

    except:
        return "OK"


# =========================
# 🌍 地圖頁（不動也可）
# =========================
@app.route("/map")
def map_page():

    html = """
    <html>
    <head><meta charset="utf-8"><title>美食地圖</title></head>
    <body style="font-family:Arial;background:#f5f5f5;margin:0">
    <div style="background:#ff6b6b;color:white;padding:20px;text-align:center">
        🍜 致理美食地圖
    </div>
    <div style="padding:20px">
        👉 請使用轉盤功能探索餐廳
    </div>
    </body>
    </html>
    """

    return html


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
