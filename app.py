from flask import Flask, request
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

# 👉 你先把自己設成會員（不然永遠不是會員）
members = [
    "Uxxxxxxxxxxxxxxxxxxxx"
]

def reply(reply_token, messages):
    payload = {
        "replyToken": reply_token,
        "messages": messages
    }

    requests.post(LINE_API, headers=headers, data=json.dumps(payload))


@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()

    event = body["events"][0]
    reply_token = event["replyToken"]
    msg = event["message"]["text"]
    user_id = event["source"]["userId"]

    # 🎡 按「美食轉盤」
    if msg == "美食轉盤":

        reply(reply_token, [
            {
                "type": "text",
                "text": "🎡 要使用美食轉盤請選擇："
            },
            {
                "type": "template",
                "altText": "會員選擇",
                "template": {
                    "type": "buttons",
                    "text": "你是會員嗎？",
                    "actions": [
                        {
                            "type": "message",
                            "label": "我是會員",
                            "text": "會員轉盤"
                        },
                        {
                            "type": "message",
                            "label": "我不是會員",
                            "text": "非會員提示"
                        }
                    ]
                }
            }
        ])

    # ✔ 會員進轉盤
    elif msg == "會員轉盤":

        if user_id in members:

            reply(reply_token, [
                {
                    "type": "text",
                    "text": "🎡 這是你的美食轉盤👇"
                },
                {
                    "type": "text",
                    "text": "https://cute-melomakarona-859d27.netlify.app"
                }
            ])

        else:

            reply(reply_token, [
                {
                    "type": "text",
                    "text": "🔒 你目前不是會員，無法使用轉盤"
                }
            ])

    # ❌ 非會員提示
    elif msg == "非會員提示":

        reply(reply_token, [
            {
                "type": "text",
                "text": "⚠️ 此功能為會員功能"
            }
        ])

    else:

        reply(reply_token, [
            {
                "type": "text",
                "text": f"收到：{msg}"
            }
        ])

    return "OK"


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
