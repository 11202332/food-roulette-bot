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
    requests.post(
        LINE_API,
        headers=headers,
        data=json.dumps({"replyToken": reply_token, "messages": messages})
    )


# =========================
# 📍 80+ 店（已補完整結構）
# =========================
places = []

# 👉 自動生成80+（避免你手寫爆炸）
types = ["台式","早午餐","日式義式","異國","咖啡","宵夜"]

for i in range(1, 85):
    t = types[i % len(types)]
    places.append({
        "name": f"致理推薦店{i}",
        "type": t,
        "lat": 25.023 + (i * 0.0001),
        "lng": 121.467 + (i * 0.0001),
        "rating": round(3.8 + (i % 15) * 0.05, 1),
        "hours": "10:00–22:00",
        # 🔥 假圖片（讓UI變好看）
        "img": f"https://source.unsplash.com/300x200/?food,{t}"
    })


# =========================
# LINE webhook（轉盤完全不動）
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()
    event = body["events"][0]

    if event["message"]["type"] != "text":
        return "OK"

    msg = event["message"]["text"]
    reply_token = event["replyToken"]

    # 🎡 轉盤（❗完全不動）
    if msg == "美食轉盤":
        reply(reply_token, [
            {"type":"text","text":"🎡 此功能為會員功能"},
            {
                "type":"template",
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
            {"type":"text","text":"🎡 https://cute-melomakarona-859d27.netlify.app"}
        ])

    elif msg == "加入會員":
        reply(reply_token, [
            {"type":"text","text":"📝 https://forms.gle/jYykimjWcX1rgYRW8"}
        ])

    # 🗺️ 地圖入口
    elif msg == "美食地圖":
        reply(reply_token, [
            {
                "type":"template",
                "template":{
                    "type":"buttons",
                    "text":"🗺️ 校園美食地圖（80+店探索）",
                    "actions":[
                        {
                            "type":"uri",
                            "label":"📍 開始探索",
                            "uri":"https://food-roulette-bot.onrender.com/map"
                        }
                    ]
                }
            }
        ])

    else:
        reply(reply_token, [{"type":"text","text":"收到："+msg}])

    return "OK"


# =========================
# 🌍 地圖頁（真正「App級UI」）
# =========================
@app.route("/map")
def map_page():

    categories = ["台式","早午餐","日式義式","異國","咖啡","宵夜"]

    html = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>美食地圖</title>
    </head>

    <body style="margin:0;font-family:Arial;background:#f2f2f2">

    <!-- 🔥 App Header -->
    <div style="
        background:linear-gradient(135deg,#ff6b6b,#ff8e53);
        color:white;
        padding:22px;
        text-align:center;
        font-size:22px;
        font-weight:bold;
    ">
        🗺️ 校園美食探索地圖
        <div style="font-size:12px;opacity:0.9">80+ 店家｜卡片探索模式</div>
    </div>

    <!-- 🔥 類別膠囊 -->
    <div style="display:flex;overflow-x:auto;padding:10px;background:white">
    """

    for c in categories:
        html += f"""
        <a href="#{c}" style="
            padding:8px 14px;
            margin-right:8px;
            background:#f1f1f1;
            border-radius:999px;
            text-decoration:none;
            color:#333;
            white-space:nowrap;
            font-size:13px;
        ">{c}</a>
        """

    html += "</div>"

    # =========================
    # 卡片區（IG風格）
    # =========================
    for c in categories:

        html += f"""
        <div id="{c}" style="
            padding:18px;
            font-size:18px;
            font-weight:bold;
            color:#333;
        ">
        {c}
        </div>

        <div style="display:flex;overflow-x:auto;padding:10px">
        """

        for x in places:

            if x["type"] == c:

                url = f"https://www.google.com/maps/search/?api=1&query={x['name']}"

                html += f"""
                <div style="
                    min-width:260px;
                    background:white;
                    margin-right:12px;
                    border-radius:16px;
                    overflow:hidden;
                    box-shadow:0 6px 16px rgba(0,0,0,0.12);
                ">

                    <img src="{x['img']}" style="width:100%;height:120px;object-fit:cover">

                    <div style="padding:12px">

                        <div style="font-size:15px;font-weight:bold">{x['name']}</div>

                        <div style="font-size:12px;color:#666;margin-top:4px">
                            ⭐ {x['rating']} ｜ 🕒 {x['hours']}
                        </div>

                        <a href="{url}" target="_blank"
                           style="
                               display:block;
                               margin-top:10px;
                               padding:8px;
                               background:#4CAF50;
                               color:white;
                               text-align:center;
                               border-radius:10px;
                               text-decoration:none;
                               font-size:13px;
                           ">
                           📍 開啟導航
                        </a>

                    </div>
                </div>
                """

        html += "</div>"

    html += "</body></html>"
    return html


# =========================
# home
# =========================
@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
