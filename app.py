from flask import Flask, request
import requests
import random

app = Flask(__name__)

LINE_TOKEN = "你的Channel Access Token"

food_list = [
    "火鍋 🍲",
    "牛肉麵 🍜",
    "便當 🍱",
    "義大利麵 🍝",
    "早餐店 🥪",
    "咖哩飯 🍛"
]

# 🎡 Flex 轉盤畫面
def flex_message(result):
    return {
        "type": "flex",
        "altText": "美食轉盤結果",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🎡 今天吃這個！", "weight": "bold", "size": "xl"},
                    {"type": "text", "text": result, "size": "xxl", "weight": "bold", "color": "#1DB446"}
                ]
            }
        }
    }

def reply(token, messages):
    url = "https://api.line.me/v2/bot/message/reply"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }

    data = {
        "replyToken": token,
        "messages": messages
    }

    requests.post(url, headers=headers, json=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    event = body["events"][0]

    reply_token = event["replyToken"]

    # 👉 點圖文選單（文字方式）
    if "message" in event:
        msg = event["message"]["text"]

        if "轉盤" in msg:
            result = random.choice(food_list)

            reply(reply_token, [
                flex_message(result)
            ])

    # 👉 如果你用 postback（進階）
    elif "postback" in event:
        data = event["postback"]["data"]

        if data == "food_roulette":
            result = random.choice(food_list)

            reply(reply_token, [
                flex_message(result)
            ])

    return "OK"


import os

if __name__ == '__main__':
    # 讓程式去讀取 Render 提供的 Port，預設找不到就用 5000
    port = int(os.environ.get("PORT", 5000))
    # 這裡最重要：host 必須改成 '0.0.0.0'
    app.run(host='0.0.0.0', port=port)
