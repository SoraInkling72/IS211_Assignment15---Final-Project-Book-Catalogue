from flask import Flask, request, redirect, render_template, flash, g
import json
from urllib.request import urlopen
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
def catalogue():
    json.dumps

@app.route('/add_to_catalogue', methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        API = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        ISBN = request.form['ISBN']

        response = urlopen(API + ISBN)
        book_data = json.load(response)

        volume_info = book_data["items"][0]["volumeInfo"]


if __name__ == "__main__":
    app.run(port=5000, debug=True)