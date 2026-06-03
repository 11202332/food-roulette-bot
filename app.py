from flask import Flask, request, abort
import requests
import os
import json

app = Flask(__name__)

# 🔑 LINE Token（換成你的）
LINE_TOKEN = "你的Channel Access Token"
LINE_API = "https://api.line.me/v2/bot/message/reply"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_TOKEN}"
}

# 👉 發送回覆
def reply(reply_token, messages):
    payload = {
        "replyToken": reply_token,
        "messages": messages
    }
    requests.post(LINE_API, headers=headers, data=json.dumps(payload))


# 📩 webhook
@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()
    print("===== BODY =====")
    print(body)

    try:
        event = body["events"][0]
        reply_token = event["replyToken"]
        msg = event["message"]["text"]

        # 🎡 美食轉盤入口
        if msg == "美食轉盤":

            reply(reply_token, [
                {
                    "type": "text",
                    "text": "🎡 幫你打開美食轉盤！"
                },
                {
                    "type": "text",
                    "text": "點下面按鈕👇",
                    "quickReply": {
                        "items": [
                            {
                                "type": "action",
                                "action": {
                                    "type": "uri",
                                    "label": "🎡 開啟轉盤",
                                    "uri": "https://cute-melomakarona-859d27.netlify.app""
                                }
                            }
                        ]
                    }
                }
            ])

        # 🧪 測試
        else:
            reply(reply_token, [
                {
                    "type": "text",
                    "text": f"收到：{msg}"
                }
            ])

        return "OK"

    except Exception as e:
        print("ERROR:", e)
        return "ERROR", 200


# 🚀 啟動
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
