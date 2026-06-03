from flask import Flask, request
import requests
import random

app = Flask(__name__)

# 🔑 換成你的 LINE Channel Access Token
LINE_TOKEN = "請貼你的Token"

# 🍔 美食清單
food_list = [
    "火鍋 🍲",
    "牛肉麵 🍜",
    "便當 🍱",
    "義大利麵 🍝",
    "早餐店 🥪",
    "咖哩飯 🍛",
    "燒肉 🍖",
    "滷肉飯 🍚"
]

# 🎡 Flex 轉盤畫面
def flex_food(result):
    return {
        "type": "flex",
        "altText": "美食轉盤結果",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🎡 今天吃這個！",
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": result,
                        "weight": "bold",
                        "size": "xxl",
                        "color": "#1DB446"
                    }
                ]
            }
        }
    }

# 📩 回覆訊息 function
def reply(reply_token, messages):
    url = "https://api.line.me/v2/bot/message/reply"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }

    data = {
        "replyToken": reply_token,
        "messages": messages
    }

    r = requests.post(url, headers=headers, json=data)
    print("reply status:", r.status_code)
    print("reply response:", r.text)


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        body = request.json
        print("BODY:", body)

        if not body or "events" not in body:
            return "OK"

        event = body["events"][0]
        reply_token = event.get("replyToken")

        msg = ""

        # 🟢 message（一般訊息）
        if "message" in event:
            msg = event["message"].get("text", "")
            print("MSG:", msg)

        # 🟡 postback（圖文選單進階）
        elif "postback" in event:
            msg = event["postback"].get("data", "")
            print("POSTBACK:", msg)

        # 🎯 判斷轉盤
        if msg and ("轉盤" in msg or "food" in msg):
            result = random.choice(food_list)

            reply(reply_token, [
                flex_food(result)
            ])

        # 🧪 測試（避免你以為壞掉）
        elif msg:
            reply(reply_token, [
                {"type": "text", "text": f"收到：{msg}"}
            ])

        return "OK"

    except Exception as e:
        print("ERROR:", str(e))
        return "OK"


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
