@app.route("/map")
def map_page():

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>致理美食手繪地圖</title>

<style>
body{
    margin:0;
    display:flex;
    height:100vh;
    font-family: "Arial";
}

/* 左側清單 */
#panel{
    width:320px;
    background:#fffaf3;
    padding:12px;
    overflow:auto;
    border-right:2px solid #eee;
}

.card{
    background:white;
    margin:8px 0;
    padding:10px;
    border-radius:14px;
    box-shadow:0 2px 6px rgba(0,0,0,0.08);
    font-size:14px;
}

/* 右側手繪地圖 */
#map{
    flex:1;
    position:relative;
    background: url("https://i.imgur.com/9Q9Z7QF.png"); /* 手繪紙張感底圖 */
    background-size:cover;
    overflow:hidden;
}

/* 區域標籤 */
.zone{
    position:absolute;
    font-size:18px;
    font-weight:bold;
    color:#5b4636;
    background:rgba(255,255,255,0.7);
    padding:4px 10px;
    border-radius:10px;
}

.z1{top:8%;left:18%;}
.z2{top:40%;left:30%;}
.z3{top:70%;left:40%;}

/* 店家點 */
.shop{
    position:absolute;
    transform:translate(-50%,-50%);
    text-align:center;
}

.pin{
    width:18px;
    height:18px;
    background:#ff6b6b;
    border-radius:50%;
    border:2px solid white;
    box-shadow:0 2px 4px rgba(0,0,0,0.2);
    margin:auto;
}

.label{
    font-size:11px;
    background:white;
    padding:2px 6px;
    border-radius:8px;
    margin-top:2px;
    display:inline-block;
}
</style>
</head>

<body>

<div id="panel">
<h3>🍜 致理美食清單</h3>
"""

    for p in places:
        html += f"""
        <div class="card">
            <b>{p['name']}</b><br>
            ⭐ {p['rating']} | {p['price']}<br>
            {p['comment']}
        </div>
        """

    html += """
</div>

<div id="map">

<div class="zone z1">文化路美食街</div>
<div class="zone z2">陽明街後門</div>
<div class="zone z3">新海路生活圈</div>
"""

    # 分區位置（手繪感，不精準但好看）
    for i, p in enumerate(places):

        zone = i % 3

        if zone == 0:
            top = 15 + (i % 10) * 6
            left = 15 + (i % 5) * 8
        elif zone == 1:
            top = 40 + (i % 10) * 5
            left = 30 + (i % 5) * 7
        else:
            top = 65 + (i % 10) * 4
            left = 50 + (i % 5) * 6

        html += f"""
        <div class="shop" style="top:{top}%;left:{left}%;">
            <div class="pin"></div>
            <div class="label">{p['name']}</div>
        </div>
        """

    html += """
</div>

</body>
</html>
"""

    return render_template_string(html)
