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

def reply(token, messages):
    requests.post(
        LINE_API,
        headers=headers,
        data=json.dumps({"replyToken": token, "messages": messages})
    )


# =========================
# 📍 真實致理周邊店（80+可再擴）
# =========================
places = [

    # 🍳 早午餐
    {"name":"麥味登致理店","type":"早午餐","img":"https://images.unsplash.com/photo-1550547660-d9450f859349"},
    {"name":"晨間廚房","type":"早午餐","img":"https://images.unsplash.com/photo-1525351484163-7529414344d8"},
    {"name":"早安美芝城","type":"早午餐","img":"https://images.unsplash.com/photo-1506084868230-bb9d95c24759"},

    # 🍱 正餐
    {"name":"油庫口麵線","type":"正餐","img":"https://images.unsplash.com/photo-1604908176997-125f25cc6f3d"},
    {"name":"金仙魯肉飯","type":"正餐","img":"https://images.unsplash.com/photo-1605478371310-a9f1c1f2b2a0"},
    {"name":"排骨大王","type":"正餐","img":"https://images.unsplash.com/photo-1604908554045-4a4b7b1f3f1e"},
    {"name":"薩莉亞","type":"正餐","img":"https://images.unsplash.com/photo-1546069901-ba9599a7e63c"},

    # ☕ 咖啡甜點
    {"name":"路易莎咖啡","type":"咖啡甜點","img":"https://images.unsplash.com/photo-1509042239860-f550ce710b93"},
    {"name":"星巴克","type":"咖啡甜點","img":"https://images.unsplash.com/photo-1495474472287-4d71bcdd2085"},
    {"name":"cama咖啡","type":"咖啡甜點","img":"https://images.unsplash.com/photo-1442512595331-e89e73853f31"},

    # 🌙 宵夜
    {"name":"阿耀臭豆腐","type":"宵夜","img":"https://images.unsplash.com/photo-1604908177522-40f7d9f3f3d1"},
    {"name":"鹽酥雞王","type":"宵夜","img":"https://images.unsplash.com/photo-1604908177522-2b5d8f3c1a9a"},
    {"name":"微笑炭烤","type":"宵夜","img":"https://images.unsplash.com/photo-1600891964599-f61ba0e24092"},
]


# =========================
# 🎡 轉盤（完全不動）
# =========================
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()
    event = data["events"][0]

    if event["message"]["type"] != "text":
        return "OK"

    msg = event["message"]["text"]
    token = event["replyToken"]

    # ❗轉盤完全不動
    if msg == "美食轉盤":
        reply(token, [
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
        reply(token, [{"type":"text","text":"🎡 https://cute-melomakarona-859d27.netlify.app"}])

    elif msg == "加入會員":
        reply(token, [{"type":"text","text":"📝 https://forms.gle/jYykimjWcX1rgYRW8"}])

    elif msg == "美食地圖":
        reply(token, [
            {
                "type":"text",
                "text":"🏫 致理科技大學美食地圖已開啟👇 https://food-roulette-bot.onrender.com/map"
            }
        ])

    else:
        reply(token, [{"type":"text","text":"收到："+msg}])

    return "OK"


# =========================
# 🗺️ 地圖頁（真正校園感 UI）
# =========================
@app.route("/map")
def map_page():

    categories = ["早午餐","正餐","咖啡甜點","宵夜"]

    html = """
    <html>
    <head>
        <meta charset="utf-8">
    </head>

    <body style="margin:0;background:#f5f6f7;font-family:Arial">

    <!-- 🏫 校園主視覺 -->
    <div style="
        background:linear-gradient(135deg,#1e3a8a,#06b6d4);
        color:white;
        padding:30px;
        text-align:center;
        font-size:26px;
        font-weight:900;
    ">
        🏫 致理科技大學
        <div style="font-size:14px;font-weight:400;margin-top:6px">
            校園周邊美食地圖（步行可達）
        </div>
    </div>

    <!-- 分類（像App） -->
    <div style="display:flex;overflow-x:auto;padding:12px;background:white">
    """

    for c in categories:
        html += f"""
        <a href="#{c}" style="
            padding:10px 16px;
            margin-right:10px;
            background:#eef2ff;
            border-radius:999px;
            text-decoration:none;
            color:#1e3a8a;
            font-weight:bold;
            white-space:nowrap;
            font-size:14px;
        ">{c}</a>
        """

    html += "</div>"

    # =========================
    # 卡片（字變大 + 地圖感）
    # =========================
    for c in categories:

        html += f"""
        <div id="{c}" style="
            padding:20px;
            font-size:22px;
            font-weight:900;
            color:#111;
        ">
        {c}
        </div>

        <div style="display:flex;overflow-x:auto;padding:12px">
        """

        for x in places:

            if x["type"] == c:

                url = f"https://www.google.com/maps/search/?api=1&query={x['name']}"

                html += f"""
                <div style="
                    min-width:300px;
                    background:white;
                    margin-right:14px;
                    border-radius:18px;
                    overflow:hidden;
                    box-shadow:0 10px 25px rgba(0,0,0,0.15);
                ">

                    <img src="{x['img']}" style="width:100%;height:150px;object-fit:cover">

                    <div style="padding:16px">

                        <div style="font-size:20px;font-weight:900">
                            {x['name']}
                        </div>

                        <a href="{url}" target="_blank"
                           style="
                               display:block;
                               margin-top:12px;
                               padding:12px;
                               background:#22c55e;
                               color:white;
                               text-align:center;
                               border-radius:12px;
                               text-decoration:none;
                               font-size:15px;
                               font-weight:bold;
                           ">
                           📍 開啟 Google Maps
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
