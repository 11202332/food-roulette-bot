from flask import Flask, render_template_string, redirect

app = Flask(__name__)

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeNgsm2AKG5z_zM4bz-lcWmyUhbWGio8EpHqCqMcfz_2kdo2A/viewform?usp=header"

DATA = {
    "文化路一段": [
        {"name":"栄次郎個人燒肉—板橋文化店","addr":"文化路一段325號","rating":"4.7","url":"https://maps.app.goo.gl/gTedZVhUR4hhw6nz6"},
        {"name":"is pasta 義大利麵","addr":"文化路一段321號","rating":"4.3","url":"https://maps.app.goo.gl/u4S4BujsEwmQRdnV7"},
        {"name":"吉飽早餐-致理店","addr":"文化路一段311-19號","rating":"4.0","url":"https://maps.app.goo.gl/ppZecPKRoRzW6VPq5"},
        {"name":"致理飯糰","addr":"文化路一段311巷24號","rating":"4.7","url":"https://maps.app.goo.gl/XBzzQkp1VuyB3fsr5"},
        {"name":"吳二麻辣鴨血","addr":"文化路一段311-6號","rating":"4.4","url":"https://maps.app.goo.gl/wTVnP3P1BeXfMweHA"},
        {"name":"吉野烤肉飯","addr":"文化路一段311-15號","rating":"3.8","url":"https://maps.app.goo.gl/4NuMrst9S6LaLsAAA"},
        {"name":"MABO POKE","addr":"文化路一段311-3號","rating":"4.3","url":"https://maps.app.goo.gl/z279YD9vMyneE4Ma9"},
        {"name":"小陳滷社","addr":"文化路一段311巷22號","rating":"3.9","url":"https://maps.app.goo.gl/1hxJG1hFFHHWA8c69"},
        {"name":"8弄5焗烤","addr":"文化路一段311-5號","rating":"3.6","url":"https://maps.app.goo.gl/yqBECv3p6rzyzA2JA"},
        {"name":"芳鄰美而美","addr":"文化路一段311-13號","rating":"4.0","url":"https://maps.app.goo.gl/nSKzHtvDUMurWkdz9"},
        {"name":"健康主義","addr":"文化路一段311-18號","rating":"4.2","url":"https://maps.app.goo.gl/wiaty6nqfMybNpMT9"},
        {"name":"龍一海南雞","addr":"文化路一段311-8號","rating":"4.6","url":"https://maps.app.goo.gl/H7s3eem2CT8p4JNJ8"},
        {"name":"晨間廚房","addr":"文化路一段311-24號","rating":"3.1","url":"https://maps.app.goo.gl/o5Xa4dFAdgjGYqM28"},
        {"name":"食尚川府","addr":"文化路一段311-21號","rating":"4.8","url":"https://maps.app.goo.gl/rhr1HHaZAV6XBR1z7"},
        {"name":"霸子牛排","addr":"文化路一段345號","rating":"4.0","url":"https://maps.app.goo.gl/4oLSG7m4w25Ehstm7"},
        {"name":"燒惑日式燒肉","addr":"文化路一段323號","rating":"4.4","url":"https://maps.app.goo.gl/aCYeMUYW4VZUrj7G7"},
    ],

    "陽明街": [
        {"name":"FlagPasta","addr":"陽明街23巷5號","rating":"4.5","url":"https://maps.app.goo.gl/yWXhhGi8tcrXd8t88"},
        {"name":"小食。候","addr":"陽明街23巷13號","rating":"4.3","url":"https://maps.app.goo.gl/WJacSW1iWu1LFiC66"},
        {"name":"義匠義式湯麵","addr":"陽明街32號","rating":"4.8","url":"https://maps.app.goo.gl/hvycV2nGZ7WKgS5e7"},
        {"name":"小松拉麵","addr":"自由路33號","rating":"4.5","url":"https://maps.app.goo.gl/LKop15YmYrWt8ccP8"},
        {"name":"一京咖哩","addr":"陽明街109號","rating":"4.6","url":"https://maps.app.goo.gl/st1Ly3jhVZiNdhZJ8"},
        {"name":"Café Wanderer","addr":"陽明街27巷7號","rating":"4.4","url":"https://maps.app.goo.gl/fY6ryS1ZkMVXLkyC9"},
        {"name":"光東养茶","addr":"陽明街131號","rating":"4.7","url":"https://maps.app.goo.gl/beXqvzWQBnMnArr66"},
        {"name":"德堡牛排","addr":"陽明街17-1號","rating":"4.0","url":"https://maps.app.goo.gl/joCCpusVhvJPYkRWA"},
    ],

    "幸福路 / 新海路": [
        {"name":"鄉親小吃","addr":"幸福路16號","rating":"4.6","url":"https://maps.app.goo.gl/cT7PFmLaPrnm2kYc8"},
        {"name":"好食堂","addr":"幸福路18號","rating":"4.2","url":"https://maps.app.goo.gl/ZQF4CXHdrNP1iHjo7"},
        {"name":"台南無刺虱目魚","addr":"新海路97號","rating":"4.4","url":"https://maps.app.goo.gl/7b41uvR3Bimf2iGR8"},
        {"name":"逸麵麵鍋燒","addr":"新海路101號","rating":"4.9","url":"https://maps.app.goo.gl/HxLnPaa2ZBqbMGRs8"},
        {"name":"牪嗑牛排","addr":"新海路63號","rating":"4.3","url":"https://maps.app.goo.gl/p9bi26hNbEpsNeS39"},
        {"name":"韓鼓韓式料理","addr":"新海路11號","rating":"4.3","url":"https://maps.app.goo.gl/UmPfLfW57evBk1Yr8"},
        {"name":"山東寶麵食館","addr":"幸福路17號","rating":"4.4","url":"https://maps.app.goo.gl/ZKpyH4qKqAuFoKpy6"},
    ]
}


HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>校園美食地圖（優化版）</title>

<style>
body{
    margin:0;
    font-family:Arial;
    background:#faf7f2;
}

/* 上方功能列 */
.topbar{
    background:#222;
    color:white;
    padding:15px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}

button{
    padding:10px 15px;
    border:none;
    cursor:pointer;
    border-radius:8px;
}

.roulette-btn{
    background:#ffcc00;
    font-weight:bold;
}

/* 左右排版 */
.container{
    display:flex;
    height:calc(100vh - 60px);
}

/* 左側分類 */
.left{
    width:35%;
    overflow:auto;
    padding:10px;
    border-right:2px solid #ddd;
}

/* 右側店家 */
.right{
    width:65%;
    overflow:auto;
    padding:10px;
}

/* 分區 */
.zone{
    margin-bottom:20px;
    background:white;
    padding:10px;
    border-radius:10px;
}

.zone h3{
    margin:5px 0;
    color:#333;
}

/* 店卡 */
.card{
    padding:8px;
    border-bottom:1px solid #eee;
}

.card a{
    color:blue;
    text-decoration:none;
}

/* modal */
.modal{
    display:none;
    position:fixed;
    top:0;left:0;
    width:100%;height:100%;
    background:rgba(0,0,0,0.5);
    justify-content:center;
    align-items:center;
}

.modal-box{
    background:white;
    padding:20px;
    border-radius:10px;
}
</style>
</head>

<body>

<div class="topbar">
    <div>🍜 校園美食地圖</div>
    <button class="roulette-btn" onclick="openModal()">會員功能轉盤</button>
</div>

<div class="container">

    <div class="left">
        {% for zone, items in data.items() %}
        <div class="zone">
            <h3>{{ zone }}</h3>
            {% for i in items %}
                <div class="card">{{ i.name }}</div>
            {% endfor %}
        </div>
        {% endfor %}
    </div>

    <div class="right">
        {% for zone, items in data.items() %}
        <div class="zone">
            <h3>{{ zone }}</h3>
            {% for i in items %}
                <div class="card">
                    <b>{{ i.name }}</b><br>
                    📍 {{ i.addr }}<br>
                    ⭐ {{ i.rating }}<br>
                    <a href="{{ i.url }}" target="_blank">Google Map</a>
                </div>
            {% endfor %}
        </div>
        {% endfor %}
    </div>

</div>

<!-- modal -->
<div class="modal" id="modal">
  <div class="modal-box">
    <h3>是否為會員？</h3>
    <button onclick="yesMember()">是會員</button>
    <button onclick="noMember()">不是會員</button>
  </div>
</div>

<script>
function openModal(){
    document.getElementById("modal").style.display="flex";
}

function yesMember(){
    alert("🎡 開啟轉盤（這裡可接你的轉盤功能）");
    document.getElementById("modal").style.display="none";
}

function noMember(){
    window.location.href = "{{ form_url }}";
}
</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML, data=DATA, form_url=FORM_URL)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
