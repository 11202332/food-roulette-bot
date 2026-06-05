@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()

    try:
        event = body["events"][0]

        if "message" not in event:
            return "OK"

        msg = event["message"]["text"]
        reply_token = event["replyToken"]

        # =====================
        # 🎡 美食轉盤（完整保留）
        # =====================
        if msg == "美食轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 會員功能"},
                {
                    "type":"template",
                    "altText":"會員選擇",
                    "template":{
                        "type":"buttons",
                        "text":"請選擇身份",
                        "actions":[
                            {"type":"message","label":"我是會員","text":"進入轉盤"},
                            {"type":"message","label":"我不是會員","text":"加入會員"}
                        ]
                    }
                }
            ])

        elif msg == "進入轉盤":
            reply(reply_token, [
                {"type":"text","text":"🎡 開啟美食轉盤👇"},
                {
                    "type":"text",
                    "text":"https://cute-melomakarona-859d27.netlify.app"
                }
            ])

        elif msg == "加入會員":
            reply(reply_token, [
                {"type":"text","text":"📝 請填寫會員表單"},
                {
                    "type":"text",
                    "text":"https://forms.gle/jYykimjWcX1rgYRW8"
                }
            ])

        # =====================
        # 🗺️ 美食地圖
        # =====================
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
            reply(reply_token, [{"type":"text","text":"收到：" + msg}])

        return "OK"

    except:
        return "OK"
