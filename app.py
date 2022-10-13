
# from crypt import methods
from email.headerregistry import Address
import os
from pickletools import long1
from queue import PriorityQueue
from flask import Flask,render_template,request,redirect,session,url_for,json

from bs4 import BeautifulSoup
import sqlite3,requests,datetime

# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory

import csv

# gittest221004


app = Flask(__name__)

app.secret_key="sunabaco"

# デバッグモードを強制True
# app.config['DEBUG']=True
app.debug = True

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/sc")
def sc():
    #スクレイピングの処理を書く
    url = "https://news.google.com/topstories?hl=ja&gl=JP&ceid=JP:ja"
    r=requests.get(url)

    soup=BeautifulSoup(r.text,"html.parser")
    
    elems=soup.find_all("a",class_="DY5T1d")
    link=soup.find_all("href")
    print(link)
    
    titlelist=[]
    
    for elem in elems:
        elem = elem.contents[0]
        titlelist.append(elem)
    
    return render_template("sc.html",html_title_list = titlelist)

# DBに接続して情報を取る
@app.route("/home")

def home():
    # DBに接続
    conn = sqlite3.connect("bouhan_map.db")
        
    #データ取得のためのカーソル作成
    c=conn.cursor()
        
    # カーソルを操作するSQLを書く
    # id=session["id"]
        
    c.execute("select * from toukou order by id DESC limit 10")
        
    # pythonに持ってくる
    toukou_data = c.fetchall()
        
    # 接続終了
    c.close()
    return render_template("home.html",html_toukou_r = toukou_data)


# @app.route("/home")

# def home():
#     if "user_id" in session:
#         # DBに接続
#         conn = sqlite3.connect("tweet.db")
        
#         #データ取得のためのカーソル作成
#         c=conn.cursor()
        
#         # カーソルを操作するSQLを書く
#         user_id=session["user_id"]
        
#         c.execute("select * from tweet where user_id = ? and deleted_id is null order by datetime asc ",(user_id,))
        
#         # pythonに持ってくる
#         tweet_data = c.fetchall()
        
#         # 接続終了
#         c.close()
#         return render_template("home.html",html_tweet_r = tweet_data)
#     else:
#         return redirect("/login")


# form.htmlへの分岐
@app.route("/form")
def form():
    return render_template("form.html")

# 投稿の処理
@app.route("/form_py",methods=["post"])
def form_post():
    # form.htmlから値を受け取る
    date = request.form.get("datetime")
    age = request.form.get("age")
    sex = request.form.get("sex")
    place = request.form.get("location_input")
    lat = request.form.get("location_conv_ido")
    lon = request.form.get("location_conv_keido")
    incident = request.form.get("class_incident")
    ForR = request.form.get("class_fact_rumor")
    detail = request.form.get("detail")
    url = request.form.get("image_url")
    # テキストの保存
    conn = sqlite3.connect("bouhan_map.db")

    # DBへ投稿内容を入力
    c=conn.cursor()
    c.execute("INSERT INTO toukou values(null,?,?,?,?,?,?,?,?,?,?)",(date,age,sex,place,lat,lon,incident,ForR,detail,url))

    # 変更を書き込み
    conn.commit()
    c.close()
    
    # home.htmlへリダイレクトさせる
    return redirect("/home")



# add
@app.route("/add")
def add():
    if "user_id" in session:
        return render_template("add.html")
    else:
        return redirect("/login")

# ポストの処理
@app.route("/add_py",methods=["post"])
def add_post():
    # HTMLから空の値を受け取る
    task=request.form.get("task")
    # 日付を取得
    date = datetime.datetime.now()
    file=request.files.get("avatar")

    if not file.filename:
        # 画像が無い時の処理

        # テキストの保存
        conn = sqlite3.connect("tweet.db")
        user_id = session["user_id"]

        c=conn.cursor()
        c.execute("INSERT INTO tweet values(null,?,?,?,null,null)",(date,task,user_id))

    else:
        # 画像があるときの処理
        # 画像の保存
        file.save(os.path.join('./static/image', file.filename))
        img_link = './static/image/' + file.filename

        # テキストの保存
        conn = sqlite3.connect("tweet.db")
        user_id = session["user_id"]

        c=conn.cursor()
        c.execute("INSERT INTO tweet values(null,?,?,?,null,?)",(date,task,user_id,img_link))


    # 変更を書き込み
    conn.commit()
    c.close()
    
    # add_pyに活かせないためにリダイレクトさせる
    return redirect("/add")

# edit
@app.route("/edit/<int:id>")

def edit(id):

    if "user_id" in session:
        # DBに接続
        conn = sqlite3.connect("tweet.db")
        
        #データ取得のためのカーソル作成
        c=conn.cursor()
        
        # カーソルを操作するSQLを書く
        c.execute("select * from tweet where id = ?",(id,))
        
        # pythonに持ってくる
        tweet_data = c.fetchall()
        
        # 接続終了
        c.close()
        return render_template("edit.html",html_tweet_data=tweet_data)
    else:
        return redirect("/login")


# 編集機能
@app.route("/edit_py", methods=["post"])
def edit_post():
    # HTMLから空の値を受け取る
    edit_task=request.form.get("task")
    edit_id = request.form.get("id")

    conn = sqlite3.connect("tweet.db")
    c=conn.cursor()

    # 日付を取得
    date = datetime.datetime.now()

    c.execute("update tweet set content = ? where id = ?",(edit_task,edit_id))

    # 変更を書き込み
    conn.commit()
    c.close()
    
    return redirect("/home")


# delete
@app.route("/delete/<int:id>")
def delete(id):
    if "user_id" in session:
        # DBに接続
        conn = sqlite3.connect("tweet.db")
        
        #データ取得のためのカーソル作成
        c=conn.cursor()
        
        # カーソルを操作するSQLを書く
        c.execute("select * from tweet where id = ?",(id,))
        
        # pythonに持ってくる
        tweet_data = c.fetchall()
        
        # 接続終了
        c.close()
        return render_template("delete.html",html_tweet_data=tweet_data)
    else:
        return redirect("/login")

# 削除機能
@app.route("/delete_py/<int:id>", methods=["post"])
def delete_post(id):
    # HTMLから空の値を受け取る
    id = int(request.form.get("id"))

    # delete_id = request.form.get("id")

    conn = sqlite3.connect("tweet.db")
    c=conn.cursor()
    
    # 論理削除
    c.execute("update tweet set deleted_id = 1 where id=?",(id,))

    # ほんとの削除
    # c.execute("delete from tweet where id = ?",(id,))

    # 変更を書き込み
    conn.commit()
    c.close()
    
    return redirect("/home")



# ログイン
@app.route("/login")
def login():
    return render_template("login.html")

# ログインの処理
@app.route("/login_py",methods=["post"])
def login_post():
    # HTMLから空の値を受け取る
    user_name = request.form.get("user_name")
    pass_word = request.form.get("pass")   
    conn = sqlite3.connect("tweet.db")
    c=conn.cursor()
    
    c.execute("select * from user where name==? and pass == ?",(user_name,pass_word))

    user=c.fetchall()
    
    c.close()
    
    # データが空じゃなかったらログインする
    if not user:
        return redirect("/login")
    else:
        session["user_id"] = user[0][0]
        return redirect("/home")
    
    print(user)
    
    # add_pyに活かせないためにリダイレクトさせる
    return redirect("/login")

# Cookieを使ってログ管理
# ページがセッションを持っているかどうか
# ⇒session["user_id"] と記述したら"user_id" in sessionで持っている
# if session["user_id"] in session:
# else:
# return redirect("/login")

# ログアウトを作る
# user_id をNoneに上書きする

@app.route("/logout")
def logout():
    # user_id = session["user_id"]
    session.pop("user_id",None)
    return redirect("/login")


# アカウント作成画面を作る
@app.route("/regist")
def regist():
    return render_template("regist.html")

@app.route("/regist_py",methods=["post"])
def regist_post():
    # HTMLから空の値を受け取る
    user_name = request.form.get("user_name")
    pass_word = request.form.get("pass")   
    conn = sqlite3.connect("tweet.db")
    c=conn.cursor()
    
    c.execute("insert into user values(Null,?,?)",(user_name,pass_word))

    # commitでデータの書き込み
    conn.commit()
    
    c.close()
    return redirect("/login")

    
@app.errorhandler(404)
def page_not_found(error):
    return "お探しのページは見つかりません！"
    
if __name__ == '__main__':
    app.run(debug=True,port=8080,use_reloader=False)


# ここから防犯マップ用の追記

@app.route("/map")
def map():
    # DBに接続
    conn = sqlite3.connect("bouhan_map.db")
    
    #データ取得のためのカーソル作成
    c=conn.cursor()
    g=conn.cursor()
    
    
    # カーソルを操作するSQLを書く
    # c.execute("select * from tweet where id = ?",(id,))
    c.execute("select * from toukou where location_conv_ido != ''")
    g.execute("select * from fukuokakenkei_opendata_add_scryping where location_conv_ido != ''")
    
    
    # pythonに持ってくる
    map_data = c.fetchall()
    map_data_opendata = g.fetchall()
    
    # 接続終了
    c.close()
    g.close()

    # 緯度・経度の形に格納
    address_dict = {}
    address_list = []

    address_dict_opendata = {}
    address_list_opendata = []
    
    for map_data_r in map_data:
        address_dict["latitude"] =map_data_r[5]
        address_dict["longitude"] = map_data_r[6]
        address_dict["incident"] = map_data_r[7] 
        address_dict["date"] = map_data_r[1][0:10]
        address_dict["class_fact_rumor"] = map_data_r[8] 
        address_dict["detail"] = map_data_r[9] 
        address_list.append(address_dict.copy())

    for map_data_r_opendata in map_data_opendata:
        address_dict_opendata["latitude"] =map_data_r_opendata[13]
        address_dict_opendata["longitude"] = map_data_r_opendata[14]
        if map_data_r_opendata[2] is None:
            address_dict_opendata["incident"] = map_data_r_opendata[1] 
        else:
            address_dict_opendata["incident"] = map_data_r_opendata[1] + "_" +map_data_r_opendata[2] 
        address_dict_opendata["date"] = map_data_r_opendata[9]
        address_dict_opendata["detail"] = map_data_r_opendata[15]
        address_dict_opendata["opendata_or_news"] = map_data_r_opendata[16]
        address_list_opendata.append(address_dict_opendata.copy())

    #確認用csv出力
    # with open('data/temp/sample_writer.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(address_list_opendata)


    # jsonファイル読み込み
    # with open('static/js/test.geojson') as f:
    #     jdata = json.load(f)
        
    return render_template("map.html",html_map_data=address_list,html_map_data_opendata=address_list_opendata)    
    
