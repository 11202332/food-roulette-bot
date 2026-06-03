from flask import Flask, request
import requests
import random
import os

app = Flask(__name__)

# 🔑 請貼你的 LINE Channel Access Token
LINE_TOKEN = "請貼你的Channel Access Token"

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

# 🎡 Flex 卡片（轉盤畫面）
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

# 📩 LINE 回覆 API
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

    print("REPLY STATUS:", r.status_code)
    print("REPLY TEXT:", r.text)


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        body = request.json
        print("===== BODY =====")
        print(body)

        if not body or "events" not in body:
            return "OK"

        event = body["events"][0]
        reply_token = event.get("replyToken")

        msg = ""

        # 🟢 一般訊息
        if "message" in event:
            msg = event["message"].get("text", "")
            print("MESSAGE:", msg)

        # 🟡 圖文選單 postback
        elif "postback" in event:
            msg = event["postback"].get("data", "")
            print("POSTBACK:", msg)

        # 🧼 清理字串（避免空格影響）
        msg = (msg or "").replace(" ", "").lower()

        print("FINAL MSG:", msg)

        # 🎯 轉盤判斷（核心）
        if msg and (
            "轉盤" in msg or
            "美食" in msg or
            "food" in msg or
            "roulette" in msg
        ):
            result = random.choice(food_list)

            reply(reply_token, [
                flex_food(result)
            ])

        # 🧪 fallback（測試用）
        elif msg:
            reply(reply_token, [
                {"type": "text", "text": f"收到：{msg}"}
            ])

        return "OK"

    except Exception as e:
        print("ERROR:", str(e))
        return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
