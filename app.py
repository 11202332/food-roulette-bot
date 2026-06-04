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
# 📌 致理美食地圖完整資料
# =========================

places = [
    # ========= 台式 / 小吃 / 便當 =========
    {"name":"致理飯糰","lat":25.0231,"lng":121.4675,"type":"台式"},
    {"name":"小陳滷味","lat":25.0232,"lng":121.4676,"type":"台式"},
    {"name":"阿房滷味","lat":25.0230,"lng":121.4672,"type":"台式"},
    {"name":"大碗公當歸羊肉","lat":25.0140,"lng":121.4620,"type":"台式"},
    {"name":"福記燒臘便當","lat":25.0135,"lng":121.4630,"type":"台式"},
    {"name":"文化小吃","lat":25.0233,"lng":121.4674,"type":"台式"},
    {"name":"皇家傳承牛肉麵","lat":25.0145,"lng":121.4635,"type":"台式"},
    {"name":"大東北牛肉麵","lat":25.0150,"lng":121.4628,"type":"台式"},
    {"name":"油庫口麵線","lat":25.0238,"lng":121.4668,"type":"台式"},
    {"name":"超吉飯桶","lat":25.0148,"lng":121.4619,"type":"台式"},
    {"name":"周二娃重慶小館","lat":25.0230,"lng":121.4670,"type":"台式"},
    {"name":"肥貓小館","lat":25.0231,"lng":121.4671,"type":"台式"},
    {"name":"山東寶麵食館","lat":25.0228,"lng":121.4669,"type":"台式"},
    {"name":"雲鼎阿二麻辣食堂","lat":25.0138,"lng":121.4632,"type":"台式"},
    {"name":"川蜀麻辣食堂","lat":25.0232,"lng":121.4677,"type":"台式"},
    {"name":"梁季港式小火鍋","lat":25.0227,"lng":121.4666,"type":"台式"},
    {"name":"麵麵牛肉麵","lat":25.0240,"lng":121.4680,"type":"台式"},
    {"name":"食八辣麻辣燙","lat":25.0142,"lng":121.4638,"type":"台式"},
    {"name":"鴨鴨金烤鴨","lat":25.0139,"lng":121.4625,"type":"台式"},
    {"name":"品榮鐵板燒","lat":25.0141,"lng":121.4627,"type":"台式"},
    {"name":"魯肉飯切仔麵","lat":25.0231,"lng":121.4673,"type":"台式"},
    {"name":"暖胃廚房","lat":25.0234,"lng":121.4676,"type":"台式"},
    {"name":"潤餅捲","lat":25.0242,"lng":121.4682,"type":"台式"},
    {"name":"陳記香菇肉粥","lat":25.0143,"lng":121.4636,"type":"台式"},
    {"name":"夢饗小吃","lat":25.0235,"lng":121.4678,"type":"台式"},

    # ========= 早午餐 =========
    {"name":"健康主義早餐","lat":25.0230,"lng":121.4670,"type":"早午餐"},
    {"name":"MABO POKE","lat":25.0136,"lng":121.4631,"type":"早午餐"},
    {"name":"萬佳鄉陽明店","lat":25.0231,"lng":121.4672,"type":"早午餐"},
    {"name":"麥哥看漢堡","lat":25.0232,"lng":121.4673,"type":"早午餐"},
    {"name":"芳鄰美而美","lat":25.0233,"lng":121.4674,"type":"早午餐"},
    {"name":"麥當勞文化店","lat":25.0236,"lng":121.4679,"type":"早午餐"},
    {"name":"心心漢堡","lat":25.0147,"lng":121.4618,"type":"早午餐"},
    {"name":"吉飽早午餐","lat":25.0139,"lng":121.4629,"type":"早午餐"},
    {"name":"麥味登致理店","lat":25.0231,"lng":121.4671,"type":"早午餐"},
    {"name":"臻甜早午餐","lat":25.0235,"lng":121.4676,"type":"早午餐"},
    {"name":"懶的享早午餐","lat":25.0237,"lng":121.4678,"type":"早午餐"},
    {"name":"雅米早午餐","lat":25.0238,"lng":121.4679,"type":"早午餐"},
    {"name":"隔壁早餐","lat":25.0229,"lng":121.4668,"type":"早午餐"},
    {"name":"厚夾吐司","lat":25.0230,"lng":121.4670,"type":"早午餐"},
    {"name":"早安公雞","lat":25.0240,"lng":121.4681,"type":"早午餐"},
    {"name":"晨間廚房","lat":25.0232,"lng":121.4672,"type":"早午餐"},

    # ========= 日式 / 義式 =========
    {"name":"Is Pasta","lat":25.0233,"lng":121.4675,"type":"日式義式"},
    {"name":"小食候","lat":25.0231,"lng":121.4672,"type":"日式義式"},
    {"name":"Flag Pasta","lat":25.0230,"lng":121.4671,"type":"日式義式"},
    {"name":"薩莉亞","lat":25.0236,"lng":121.4678,"type":"日式義式"},
    {"name":"甘泉魚麵","lat":25.0235,"lng":121.4677,"type":"日式義式"},
    {"name":"Sukiya","lat":25.0234,"lng":121.4676,"type":"日式義式"},
    {"name":"宮本武丼","lat":25.0138,"lng":121.4628,"type":"日式義式"},
    {"name":"坐一下吧","lat":25.0140,"lng":121.4630,"type":"日式義式"},
    {"name":"豚將拉麵","lat":25.0142,"lng":121.4632,"type":"日式義式"},
    {"name":"双豚拉麵","lat":25.0135,"lng":121.4625,"type":"日式義式"},
    {"name":"勇氣食堂","lat":25.0230,"lng":121.4670,"type":"日式義式"},
    {"name":"津之芳生魚片","lat":25.0231,"lng":121.4671,"type":"日式義式"},
    {"name":"小吉咖哩","lat":25.0232,"lng":121.4672,"type":"日式義式"},
    {"name":"幸輝共榮食堂","lat":25.0241,"lng":121.4683,"type":"日式義式"},

    # ========= 異國 =========
    {"name":"蘊涵廣東腸粉","lat":25.0139,"lng":121.4629,"type":"異國"},
    {"name":"韓鼓韓式料理","lat":25.0230,"lng":121.4670,"type":"異國"},
    {"name":"成記越式麵疙瘩","lat":25.0138,"lng":121.4628,"type":"異國"},
    {"name":"清心越南料理","lat":25.0137,"lng":121.4627,"type":"異國"},
    {"name":"泰品味","lat":25.0231,"lng":121.4671,"type":"異國"},

    # ========= 咖啡廳 =========
    {"name":"初見咖啡","lat":25.0230,"lng":121.4670,"type":"咖啡"},
    {"name":"貓欸咖啡","lat":25.0231,"lng":121.4671,"type":"咖啡"},
    {"name":"咖啡浪遊","lat":25.0232,"lng":121.4672,"type":"咖啡"},
    {"name":"路易莎","lat":25.0233,"lng":121.4673,"type":"咖啡"},
    {"name":"DOSE Coffee","lat":25.0240,"lng":121.4680,"type":"咖啡"},
    {"name":"一室咖啡","lat":25.0234,"lng":121.4674,"type":"咖啡"},
    {"name":"星巴克","lat":25.0236,"lng":121.4676,"type":"咖啡"},
    {"name":"BEGIN AGAIN","lat":25.0237,"lng":121.4677,"type":"咖啡"},
    {"name":"米妲咖啡","lat":25.0238,"lng":121.4678,"type":"咖啡"},
    {"name":"起點咖啡","lat":25.0235,"lng":121.4675,"type":"咖啡"},
    {"name":"和泰興麵包","lat":25.0239,"lng":121.4679,"type":"咖啡"},
    {"name":"卷卷烘焙","lat":25.0241,"lng":121.4681,"type":"咖啡"},
    {"name":"鴉片粉圓","lat":25.0242,"lng":121.4682,"type":"咖啡"},
    {"name":"車輪餅","lat":25.0243,"lng":121.4683,"type":"咖啡"},
    {"name":"雞蛋糕","lat":25.0244,"lng":121.4684,"type":"咖啡"},
    {"name":"紅豆餅","lat":25.0245,"lng":121.4685,"type":"咖啡"},

    # ========= 宵夜 =========
    {"name":"微笑炭烤","lat":25.0140,"lng":121.4620,"type":"宵夜"},
    {"name":"阿耀臭豆腐","lat":25.0141,"lng":121.4621,"type":"宵夜"},
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
