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

    # 🎡 點「美食轉盤」
    if msg == "美食轉盤":

        reply(reply_token, [
            {
                "type": "text",
                "text": "🎡 此功能為會員功能"
            },
            {
                "type": "template",
                "altText": "會員選擇",
                "template": {
                    "type": "buttons",
                    "text": "請選擇身份",
                    "actions": [
                        {
                            "type": "message",
                            "label": "我是會員",
                            "text": "進入轉盤"
                        },
                        {
                            "type": "message",
                            "label": "我不是會員",
                            "text": "加入會員"
                        }
                    ]
                }
            }
        ])

    # ✔ 不管是不是會員 → 都可以進轉盤
    elif msg == "進入轉盤":

        reply(reply_token, [
            {
                "type": "text",
                "text": "🎡 開啟美食轉盤👇"
            },
            {
                "type": "text",
                "text": "https://cute-melomakarona-859d27.netlify.app"
            }
        ])

    # ❌ 加入會員
    elif msg == "加入會員":

        reply(reply_token, [
            {
                "type": "text",
                "text": "📝 請填寫會員表單"
            },
            {
                "type": "text",
                "text": "https://forms.gle/jYykimjWcX1rgYRW8"
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
