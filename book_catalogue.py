from flask import Flask, request, redirect, render_template, flash, g
import re
import sqlite3

app = Flask(__name__)
app.secret_key = 'sprigatito906'

@app.route('/')
def index():
    return render_template("user_login.html")

@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # validate username & password
        if username == "admin" and password == "password":
            return redirect('/catalogue_dashboard')
        else:
            flash("Please input correct credentials")
            return redirect('/')
    return render_template("user_login.html")

@app.route('/catalogue_dashboard', methods=["GET", "POST"])
def dashboard():


#if __name__ == "__main__":
    app.run(port=5000, debug=True)