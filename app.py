
import os
from queue import PriorityQueue
from flask import Flask,render_template,request,redirect,session,url_for

from bs4 import BeautifulSoup
import sqlite3,requests,datetime

# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory

# gittest221004


app = Flask(__name__)

app.secret_key="sunabaco"

# デバッグモードを強制True
# app.config['DEBUG']=True
app.debug = True

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/goodbye")
def good_bye():
    return "<p>GoodBye</p>"

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
    if "user_id" in session:
        # DBに接続
        conn = sqlite3.connect("tweet.db")
        
        #データ取得のためのカーソル作成
        c=conn.cursor()
        
        # カーソルを操作するSQLを書く
        user_id=session["user_id"]
        
        c.execute("select * from tweet where user_id = ? and deleted_id is null order by datetime asc ",(user_id,))
        
        # pythonに持ってくる
        tweet_data = c.fetchall()
        
        # 接続終了
        c.close()
        return render_template("home.html",html_tweet_r = tweet_data)
    else:
        return redirect("/login")

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
    app.run(debug=True,  use_reloader=False)


# 論理削除
# 削除が確認してから実行されるように
# 画像をアップロード、表示できるようにしてください。
