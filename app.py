from flask import Flask, request
import requests
import random
import os

app = Flask(__name__)

# 🔑 LINE Token（一定要換成你自己的）
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

# 🎡 Flex卡片
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

# 📩 reply function（已加 debug）
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

    print("==== REPLY DEBUG ====")
    print("STATUS:", r.status_code)
    print("TEXT:", r.text)


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        body = request.get_json(force=True, silent=True)

        print("===== BODY =====")
        print(body)

        if not body:
            return "OK"

        events = body.get("events", [])
        if not events:
            return "OK"

        event = events[0]

        reply_token = event.get("replyToken")
        if not reply_token:
            return "OK"

        msg = ""

        # 🟢 message
        if event.get("message"):
            msg = event["message"].get("text", "")

        # 🟡 postback
        elif event.get("postback"):
            msg = event["postback"].get("data", "")

        print("RAW MSG:", msg)

        msg = (msg or "").replace(" ", "").lower()

        # 🎯 轉盤判斷
        if ("轉盤" in msg or "美食" in msg or "food" in msg or "roulette" in msg):

            result = random.choice(food_list)

            reply(reply_token, [
                flex_food(result)
            ])

        else:
            reply(reply_token, [
                {"type": "text", "text": f"收到：{msg}"}
            ])

        return "OK"

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
