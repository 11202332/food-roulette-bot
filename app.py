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


# =========================
# 📌 美食資料（80家你可自行擴充）
# =========================
places = [

    {"name":"致理飯糰","lat":25.0231,"lng":121.4675,"type":"台式","rating":4.3,"reviews":120,"hours":"06:30–10:30"},
    {"name":"小陳滷味","lat":25.0232,"lng":121.4676,"type":"台式","rating":4.5,"reviews":210,"hours":"17:00–23:30"},
    {"name":"阿房滷味","lat":25.0230,"lng":121.4672,"type":"台式","rating":4.2,"reviews":180,"hours":"16:30–23:00"},
    {"name":"文化小吃","lat":25.0233,"lng":121.4674,"type":"台式","rating":4.1,"reviews":98,"hours":"10:00–20:00"},
    {"name":"油庫口麵線","lat":25.0238,"lng":121.4668,"type":"台式","rating":4.6,"reviews":3200,"hours":"09:00–18:00"},

    {"name":"麥味登致理店","lat":25.0231,"lng":121.4671,"type":"早午餐","rating":4.0,"reviews":260,"hours":"06:00–13:30"},
    {"name":"麥當勞文化店","lat":25.0236,"lng":121.4679,"type":"早午餐","rating":4.2,"reviews":980,"hours":"24小時"},
    {"name":"晨間廚房","lat":25.0232,"lng":121.4672,"type":"早午餐","rating":4.1,"reviews":340,"hours":"06:00–14:00"},

    {"name":"Is Pasta","lat":25.0233,"lng":121.4675,"type":"日式義式","rating":4.3,"reviews":210,"hours":"11:00–21:30"},
    {"name":"薩莉亞","lat":25.0236,"lng":121.4678,"type":"日式義式","rating":4.1,"reviews":530,"hours":"11:00–22:00"},
    {"name":"Sukiya","lat":25.0234,"lng":121.4676,"type":"日式義式","rating":4.4,"reviews":410,"hours":"24小時"},

    {"name":"韓鼓韓式料理","lat":25.0230,"lng":121.4670,"type":"異國","rating":4.3,"reviews":320,"hours":"11:00–21:00"},
    {"name":"泰品味","lat":25.0231,"lng":121.4671,"type":"異國","rating":4.2,"reviews":210,"hours":"11:00–21:00"},

    {"name":"路易莎","lat":25.0233,"lng":121.4673,"type":"咖啡","rating":4.4,"reviews":620,"hours":"07:00–21:00"},
    {"name":"星巴克","lat":25.0236,"lng":121.4676,"type":"咖啡","rating":4.5,"reviews":890,"hours":"07:00–22:00"},

    {"name":"微笑炭烤","lat":25.0140,"lng":121.4620,"type":"宵夜","rating":4.3,"reviews":150,"hours":"18:00–01:00"},
    {"name":"阿耀臭豆腐","lat":25.0141,"lng":121.4621,"type":"宵夜","rating":4.2,"reviews":180,"hours":"17:00–00:30"},
]


# =========================
# LINE webhook
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    body = request.get_json()

    try:
        event = body["events"][0]

        if "message" not in event:
            return "OK"

        if event["message"]["type"] != "text":
            return "OK"

        reply_token = event["replyToken"]
        msg = event["message"]["text"]

        # =========================
        # 🎡 轉盤（❗完全不動）
        # =========================
        if msg == "美食轉盤":

            reply(reply_token, [
                {"type":"text","text":"🎡 此功能為會員功能"},
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
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        elif msg == "加入會員":

            reply(reply_token, [
                {"type":"text","text":"📝 請填寫會員表單"},
                {"type":"text","text":"https://forms.gle/jYykimjWcX1rgYRW8"}
            ])

        # =========================
        # 🗺️ 地圖入口（優化UI）
        # =========================
        elif msg == "美食地圖":

            reply(reply_token, [
                {
                    "type": "template",
                    "altText": "美食地圖",
                    "template": {
                        "type": "buttons",
                        "text": "🗺️ 致理美食地圖已開啟",
                        "actions": [
                            {
                                "type": "uri",
                                "label": "📍 開啟地圖",
                                "uri": "https://food-roulette-bot.onrender.com/map"
                            }
                        ]
                    }
                }
            ])

        else:

            reply(reply_token, [
                {"type":"text","text":"收到：" + msg}
            ])

        return "OK"

    except:
        return "OK"


# =========================
# 🌍 地圖頁（真正地圖App UI）
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

    <body style="margin:0;font-family:Arial;background:#f5f5f5">

    <div style="
        background:#ff6b6b;
        color:white;
        padding:18px;
        text-align:center;
        font-size:22px;
    ">
        🗺️ 致理周邊美食地圖
        <div style="font-size:13px">可滑動卡片｜點擊導航</div>
    </div>

    <!-- 🔥 分類列 -->
    <div style="
        display:flex;
        overflow-x:auto;
        padding:10px;
        background:white;
        position:sticky;
        top:0;
    ">
    """

    for c in categories:
        html += f"""
        <a href="#{c}" style="
            padding:8px 12px;
            margin-right:8px;
            background:#eee;
            border-radius:20px;
            text-decoration:none;
            color:#333;
            white-space:nowrap;
        ">{c}</a>
        """

    html += "</div>"

    # =========================
    # 卡片區
    # =========================
    for c in categories:

        html += f"""
        <div id="{c}" style="padding:15px;font-size:18px;font-weight:bold">
            {c}
        </div>

        <div style="display:flex;overflow-x:auto;padding:10px">
        """

        for x in places:

            if x["type"] == c:

                maps_url = f"https://www.google.com/maps/search/?api=1&query={x['name']} {x['lat']},{x['lng']}"

                html += f"""
                <div style="
                    min-width:220px;
                    background:white;
                    margin-right:12px;
                    padding:12px;
                    border-radius:14px;
                    box-shadow:0 3px 8px rgba(0,0,0,0.08)
                ">

                    <div style="font-weight:bold;font-size:16px">{x['name']}</div>

                    <div style="font-size:12px;color:#666;margin-top:4px">
                        ⭐ {x['rating']} ｜ {x['reviews']} 評論
                    </div>

                    <div style="font-size:12px;color:#666">
                        🕒 {x['hours']}
                    </div>

                    <a href="{maps_url}" target="_blank"
                       style="
                           display:block;
                           margin-top:10px;
                           text-align:center;
                           padding:6px;
                           background:#4CAF50;
                           color:white;
                           border-radius:8px;
                           text-decoration:none;
                       ">
                       📍 導航
                    </a>

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
