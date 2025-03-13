from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd

app = Flask(__name__)
app.secret_key = 'admin'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def hello():
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
    session['is_user_admin'] = False
    if request.method == "POST":
        users = pd.read_csv('statics/db/users.csv')
        if (request.form.get("user_id") in users['user_id'].values and request.form.get("user_pw") in users['user_pw'].values):
            session['is_user_admin'] = True
            return redirect(url_for('admin'))
            
    return render_template("login.html")

@app.route('/result')
def result():
    name = session.get('user_name','Guest')
    subscribe = session.get('user_subscription', 'No') 
    return render_template("result.html", name=name, subscribe=subscribe)

@app.route('/admin')
def admin():
    if (session["is_user_admin"]):
        return render_template("admin.html")
    else:
        return redirect(url_for('login'))

@app.route('/clear')
def clear():
    session.clear()
    print(session)
    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(debug=True)
