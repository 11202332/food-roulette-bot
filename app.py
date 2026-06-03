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

# ⭐ 假會員資料（之後可以改成資料庫）
members = []

def reply(reply_token, messages):
    payload = {
        "replyToken": reply_token,
        "messages": messages
    }
    requests.post(LINE_API, headers=headers, data=json.dumps(payload))


@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()
    print("===== BODY =====")
    print(body)

    try:
        event = body["events"][0]
        reply_token = event["replyToken"]
        msg = event["message"]["text"]
        user_id = event["source"]["userId"]

        # 🎡 美食轉盤
        if msg == "美食轉盤":

            # ✔ 會員
            if user_id in members:

                reply(reply_token, [
                    {
                        "type": "text",
                        "text": "🎡 歡迎會員使用美食轉盤！"
                    },
                    {
                        "type": "text",
                        "text": "👉 點這裡開啟轉盤："
                    },
                    {
                        "type": "text",
                        "text": "https://cute-melomakarona-859d27.netlify.app"
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
                        "text": "📌 請先完成註冊＋繳費"
                    },
                    {
                        "type": "text",
                        "text": "📝 表單：https://https://forms.gle/jYykimjWcX1rgYRW8"
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
        print("ERROR:", e)
        return "ERROR", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
