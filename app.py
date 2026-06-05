from flask import Flask, request, render_template_string
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
# 🍜 店家資料（致理校園版）
# =========================
places = [
# ========== 文化路一段（正門核心） ==========
{"name":"栄次郎個人燒肉","lat":25.0256,"lng":121.4658,"type":"燒肉","rating":4.7,"price":"$200-400","desc":"文化路燒肉","comment":"想吃肉直接來這間，自己烤超爽但錢包會痛，適合獎學金或發薪日犒賞自己"},
{"name":"FlagPasta","lat":25.0254,"lng":121.4649,"type":"義大利麵","rating":4.5,"price":"$200-400","comment":"義大利麵穩定好吃，份量偏剛好，適合不想吃太重口味的午餐"},
{"name":"小食。候","lat":25.0252,"lng":121.4645,"type":"咖啡廳","rating":4.3,"price":"$200-400","comment":"環境安靜很適合讀書，但座位不多，期末會被佔滿"},
{"name":"義匠義式湯麵","lat":25.0250,"lng":121.4639,"type":"義大利麵","rating":4.8,"price":"$200-400","comment":"湯麵很特別，味道濃但不膩，算是會想回訪的店"},
{"name":"is pasta","lat":25.0248,"lng":121.4635,"type":"義大利麵","rating":4.3,"price":"$200-400","comment":"平價義大利麵，學生聚餐很常選這間"},
{"name":"吉飽早餐","lat":25.0246,"lng":121.4632,"type":"早餐","rating":4.0,"price":"$1-200","comment":"早八救星，出餐快，趕課不會遲到"},
{"name":"致理飯糰","lat":25.0245,"lng":121.4629,"type":"早餐","rating":4.7,"price":"$1-200","comment":"飯糰超大顆，CP值高，是致理學生早餐第一名"},
{"name":"吳二麻辣鴨血","lat":25.0243,"lng":121.4626,"type":"小吃","rating":4.4,"price":"$1-200","comment":"辣度可以調整，冬天吃超暖"},
{"name":"吉野烤肉飯","lat":25.0241,"lng":121.4623,"type":"便當","rating":3.8,"price":"$1-200","comment":"便當穩定但不驚艷，趕時間會買"},
{"name":"MABO POKE","lat":25.0239,"lng":121.4621,"type":"健康餐","rating":4.3,"price":"$1-200","comment":"健身或想吃清爽的會來這，女生很愛"},

# ========== 陽明街（後門主戰區） ==========
{"name":"一京咖哩","lat":25.0240,"lng":121.4640,"type":"咖哩","rating":4.6,"price":"$1-200","comment":"咖哩濃郁，CP值很高，學生很常排隊"},
{"name":"小陳滷社","lat":25.0237,"lng":121.4637,"type":"滷味","rating":3.9,"price":"$1-200","comment":"宵夜滷味，選擇多但口味偏清淡"},
{"name":"Café Wanderer","lat":25.0235,"lng":121.4634,"type":"咖啡廳","rating":4.4,"price":"$200-400","comment":"文青咖啡廳，很適合拍照跟讀書"},
{"name":"海雲韓式料理","lat":25.0232,"lng":121.4631,"type":"韓式","rating":4.7,"price":"$400-600","comment":"韓式炸雞跟鍋類都很強，適合聚餐"},
{"name":"NU PASTA","lat":25.0230,"lng":121.4628,"type":"義大利麵","rating":4.6,"price":"$200-400","comment":"學生聚餐安全牌，穩定不踩雷"},
{"name":"光東養茶","lat":25.0228,"lng":121.4625,"type":"飲料","rating":4.7,"price":"$1-200","comment":"茶味很香，不會太甜"},
{"name":"川蜀麻辣食堂","lat":25.0226,"lng":121.4622,"type":"麻辣","rating":4.3,"price":"$200-400","comment":"喜歡重口味會愛，辣度很有感"},
{"name":"文化小吃","lat":25.0224,"lng":121.4619,"type":"小吃","rating":3.9,"price":"$1-200","comment":"便宜大碗，學生月底救星"},
{"name":"芳鄰美而美","lat":25.0222,"lng":121.4616,"type":"早餐","rating":4.0,"price":"$1-200","comment":"傳統早餐店，早八必備"},
{"name":"麻丹辣小火鍋","lat":25.0220,"lng":121.4613,"type":"火鍋","rating":4.9,"price":"$200-400","comment":"湯頭很強，學生聚餐超熱門"},

# ========== 新海路（外圍生活圈） ==========
{"name":"好食堂","lat":25.0268,"lng":121.4660,"type":"便當","rating":4.2,"price":"$1-200","comment":"便當份量大，男生很愛"},
{"name":"韓鼓韓式料理","lat":25.0270,"lng":121.4663,"type":"韓式","rating":4.3,"price":"$400-600","comment":"韓式料理偏高價但品質不錯"},
{"name":"牪嗑牛排","lat":25.0272,"lng":121.4666,"type":"牛排","rating":4.3,"price":"$200-400","comment":"學生牛排店，CP值可以"},
{"name":"龍一海南雞","lat":25.0274,"lng":121.4669,"type":"便當","rating":4.6,"price":"$1-200","comment":"海南雞飯很嫩，很多人外帶"},
{"name":"逸麵鍋燒","lat":25.0276,"lng":121.4672,"type":"鍋燒","rating":4.9,"price":"$1-200","comment":"湯頭超強，冬天必吃"}
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

        msg = event["message"]["text"]
        reply_token = event["replyToken"]

        # =====================
        # 🎡 轉盤（完整保留）
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
                {"type":"text","text":"https://cute-melomakarona-859d27.netlify.app"}
            ])

        elif msg == "加入會員":
            reply(reply_token, [
                {"type":"text","text":"📝 請填寫會員表單"},
                {"type":"text","text":"https://forms.gle/jYykimjWcX1rgYRW8"}
            ])

        # =====================
        # 🗺️ 地圖入口
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


# =========================
# 🌍 MAP（穩定 Leaflet 版本）
# =========================
@app.route("/map")
def map_page():

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>致理美食地圖</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
body {{
    margin:0;
    font-family:Arial;
    display:flex;
    height:100vh;
}}

#map {{
    flex:1;
}}

#panel {{
    width:340px;
    overflow:auto;
    background:#fafafa;
    padding:10px;
}}

.card {{
    background:white;
    margin:8px 0;
    padding:10px;
    border-radius:12px;
    cursor:pointer;
    transition:0.2s;
}}

.card:hover {{
    transform:scale(1.02);
}}

.active {{
    border:2px solid #ff6b6b;
}}
</style>

</head>

<body>

<div id="map"></div>

<div id="panel">
<h3>🍜 致理美食地圖</h3>
"""

    for i,p in enumerate(places):
        html += f"""
        <div class="card" onclick="focusMarker({i})">
            <b>{p['name']}</b><br>
            ⭐ {p['rating']} | {p['price']}<br>
            {p['desc']}
        </div>
        """

    html += """
</div>

<script>

const map = L.map('map').setView([25.0213, 121.4625], 18);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    minZoom: 17
}).addTo(map);

const places = """ + json.dumps(places, ensure_ascii=False) + """;

let markers = [];

const iconColor = {
    "台式":"red",
    "早午餐":"blue",
    "日式":"green",
    "咖啡":"orange"
};

places.forEach((p, i) => {

    const icon = L.divIcon({
        className:"",
        html:`<div style="
            width:12px;height:12px;
            background:${iconColor[p.type] || "gray"};
            border-radius:50%;
            border:2px solid white;
            box-shadow:0 0 4px rgba(0,0,0,0.4);
        "></div>`,
        iconSize:[12,12],
        iconAnchor:[6,6]
    });

    const m = L.marker([p.lat, p.lng], {icon}).addTo(map)
        .bindPopup(`<b>${p.name}</b><br>${p.desc}`);

    m.on('click', () => highlightCard(i));

    markers.push(m);
});

function focusMarker(i){
    map.setView([places[i].lat, places[i].lng], 19);
    markers[i].openPopup();
    highlightCard(i);
}

function highlightCard(i){
    document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.card')[i].classList.add('active');
    document.querySelectorAll('.card')[i].scrollIntoView({
        behavior:'smooth',
        block:'center'
    });
}

</script>

</body>
</html>
"""

    return render_template_string(html)


# =========================
# home
# =========================
@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
