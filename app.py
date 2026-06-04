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
# 🍜 美食資料（你全部原始資料完整保留）
# =========================
foodData = [
    {"n":"吉飽早餐","a":"文化路311-19號","t":"早餐"},
    {"n":"致理飯糰","a":"文化路311巷24號","t":"早餐"},
    {"n":"芳鄰美而美","a":"文化路311-13號","t":"早餐"},
    {"n":"健康主義","a":"文化路311-18號","t":"早餐"},
    {"n":"達利早餐","a":"文化路313號","t":"早餐"},
    {"n":"麥味登","a":"文化路","t":"早餐"},
    {"n":"拉亞漢堡","a":"文化路","t":"早餐"},
    {"n":"Q Burger","a":"文化路","t":"早餐"},
    {"n":"永和豆漿","a":"新埔","t":"早餐"},
    {"n":"向陽晨間","a":"漢生西路","t":"早餐"},

    {"n":"禾吉屋丼飯","a":"陽明街","t":"正餐"},
    {"n":"一京咖哩","a":"陽明街","t":"正餐"},
    {"n":"MABO POKE","a":"311-3號","t":"正餐"},
    {"n":"夢饗小吃","a":"311-16號","t":"正餐"},
    {"n":"吉野烤肉飯","a":"311-15號","t":"正餐"},
    {"n":"8鍋臭臭鍋","a":"漢生西路","t":"正餐"},
    {"n":"麻丹辣火鍋","a":"漢生西路","t":"正餐"},
    {"n":"燒惑燒肉","a":"文化路","t":"正餐"},
    {"n":"榮次郎燒肉","a":"文化路","t":"正餐"},
    {"n":"小食候","a":"陽明街","t":"正餐"},

    {"n":"Coffee HABU","a":"光正街","t":"點心"},
    {"n":"點點甜甜","a":"光正街","t":"點心"},
    {"n":"五桐號","a":"文化路","t":"點心"},
    {"n":"可不可熟成紅茶","a":"新埔","t":"點心"},
    {"n":"迷客夏","a":"新埔","t":"點心"},
    {"n":"星巴克","a":"板橋車站","t":"點心"},

    {"n":"小陳滷味","a":"311巷","t":"宵夜"},
    {"n":"鹽酥雞","a":"漢生西路","t":"宵夜"},
    {"n":"吳二麻辣鴨血","a":"311-6號","t":"宵夜"},
    {"n":"串燒店","a":"文化路","t":"宵夜"},
    {"n":"炸雞排","a":"新埔","t":"宵夜"},
    {"n":"滷味攤","a":"文化路","t":"宵夜"},
    {"n":"麻辣燙","a":"漢生西路","t":"宵夜"},
    {"n":"關東煮","a":"文化路","t":"宵夜"},
    {"n":"夜間麵店","a":"文化路","t":"宵夜"},
    {"n":"炸物攤","a":"文化路","t":"宵夜"}
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

        # 🎡 轉盤（保留你原本）
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

        # 🗺️ 地圖入口
        elif msg == "美食地圖":

            reply(reply_token, [{
                "type": "template",
                "altText": "美食地圖",
                "template": {
                    "type": "buttons",
                    "text": "🍜 致理周邊美食地圖已開啟",
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

            reply(reply_token, [
                {"type":"text","text":"收到：" + msg}
            ])

        return "OK"

    except:
        return "OK"


# =========================
# 🌍 地圖頁（完整版）
# =========================
@app.route("/map")
def map_page():

    categories = ["早餐", "正餐", "點心", "宵夜"]

    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>致理美食地圖</title>
    </head>

    <body style="margin:0;font-family:Arial;background:#f5f5f5">

    <div style="background:#ff6b6b;color:white;padding:18px;text-align:center;font-size:22px">
        🍜 致理周邊美食地圖
        <div style="font-size:13px;margin-top:5px">學生步行美食探索系統</div>
    </div>
    """

    for c in categories:

        html += f"""
        <div style="margin:12px;font-size:18px;font-weight:bold;color:#333">
        📍 {c}
        </div>
        """

        for x in foodData:

            if x["t"] == c:

                maps_url = f"https://www.google.com/maps/search/{x['n']} {x['a']}"

                html += f"""
                <div style="
                    background:white;
                    margin:10px;
                    padding:12px;
                    border-radius:12px;
                    box-shadow:0 2px 6px rgba(0,0,0,0.1)
                ">

                    <div style="color:#ff6b6b;font-weight:bold;font-size:13px">
                        {x['t']}
                    </div>

                    <h3 style="margin:6px 0">{x['n']}</h3>

                    <p style="margin:5px 0;color:#555">
                        📍 {x['a']}
                    </p>

                    <a href="{maps_url}" target="_blank"
                       style="
                       display:inline-block;
                       margin-top:6px;
                       padding:6px 10px;
                       background:#4CAF50;
                       color:white;
                       border-radius:6px;
                       text-decoration:none;
                       font-size:13px
                       ">
                       🚗 Google Maps 導航
                    </a>

                </div>
                """

    html += """
    </body>
    </html>
    """

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
