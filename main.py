from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import dotenv
import os

from py_libs import user_tools, csv_tools, secure_tools

dotenv.load_dotenv('/home/galesky/Documents/GitHub/server/python_server/statics/db/key.env')
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        user_pw = request.form.get("user_pw")
        admin_inquire = "admin" if request.form.get("admin_inquire") else None
        
        try:
            if admin_inquire:
                new_user = user_tools.User_cookies(user_id, user_pw, authorities=set({admin_inquire}))
            else:
                new_user = user_tools.User_cookies(user_id, user_pw)
            
            csv_tools.append_csv('statics/db/users.csv', new_user.get_cookies())

            return redirect(url_for('login'))

        except Exception as e:
            return render_template("error_page.html", error_msg = f"회원가입 중 오류 발생: {e}")

    return render_template("sign_up.html")

@app.route('/about')
def about():
    print('user got in about')
    return render_template("about.html")

@app.route('/form', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        session['user_name'] = request.form.get("first_name") + request.form.get('last_name')
        session['user_subscription'] = "Yes" if request.form.get("subscribe") else "No"
        return redirect(url_for('result'))
    return render_template("form.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = pd.read_csv('statics/db/users.csv')

        for idx, val in enumerate(users['user_id'].values):
            print(idx, val)
            if (request.form.get("user_id") == val \
                and users['user_pw'].values[idx] == str(secure_tools.encryption(request.form.get("user_pw")))):
                session = {"authorities":users['authorities'][idx]}
                print(session)
                print("NOTICE:: PASSED!")
                return redirect(url_for('admin'))
            
    return render_template("login.html")

@app.route('/admin')
def admin():
    if (session.get('authorities', False)):
        return render_template("admin.html")
    else:
        return redirect(url_for('login'))

@app.route('/result')
def result():
    name = session.get('user_name','Guest')
    subscribe = session.get('user_subscription', 'No') 
    return render_template("result.html", name=name, subscribe=subscribe)

@app.route('/clear')
def clear():
    session.clear()
    print(session)
    return redirect(url_for('form'))


if __name__ == '__main__':
    print(os.getenv('SECRET_KEY'))
    app.run(debug=True)
