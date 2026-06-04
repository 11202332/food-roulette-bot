from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# LINE Token（Render 環境變數）
LINE_TOKEN = os.environ.get("LINE_TOKEN")

LINE_API = "https://api.line.me/v2/bot/message/reply"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_TOKEN}"
}

# ⭐ 會員清單（你之後把 userId 加進來）
members = [
    # "Uxxxxxxxxxxxxxxxxxxxx"
]

def reply(reply_token, messages):

    payload = {
        "replyToken": reply_token,
        "messages": messages
    }

    res = requests.post(
        LINE_API,
        headers=headers,
        data=json.dumps(payload)
    )

    print("STATUS =", res.status_code)
    print("RESPONSE =", res.text)


@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()
    print("BODY =", body)

    try:
        event = body["events"][0]

        reply_token = event["replyToken"]
        msg = event["message"]["text"]
        user_id = event["source"]["userId"]

        print("MSG =", msg)
        print("USER_ID =", user_id)

        # 🎡 美食轉盤功能
        if msg == "美食轉盤":

            # ✔ 會員
            if user_id in members:

                reply(reply_token, [
                    {
                        "type": "text",
                        "text": "🎡 這是你的美食轉盤"
                    },
                    {
                        "type": "text",
                        "text": "👉 https://cute-melomakarona-859d27.netlify.app"
                    }
                ])

            # ❌ 非會員
            else:

                reply(reply_token, [
                    {
                        "type": "text",
                        "text": "🔒 此功能為會員限定"
                    },
                    {
                        "type": "text",
                        "text": "📌 請加入會員才能使用轉盤"
                    },
                    {
                        "type": "text",
                        "text": "📝 加入會員表單：https://forms.gle/jYykimjWcX1rgYRW8"
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

    except Exception as e:
        print("ERROR =", str(e))
        return "OK"


@app.route("/")
def home():
    return "Bot is running"


# 🚀 啟動
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)
