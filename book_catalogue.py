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
    with open() as book:
        book_list = json.load(book)

    print(book_list)


@app.route('/add_to_catalogue', methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        API = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        ISBN = request.form['ISBN']

        response = urlopen(API + ISBN)
        book_data = json.load(response)

        volume_info = book_data["items"][0]["volumeInfo"]
        title = volume_info["title"]
        authors = volume_info["authors"]
        prettify_author = authors if len(authors) > 1 else authors[0]
        page_count = volume_info["pageCount"]

        book_list = json.load()
        book_list.append({"title": title, "authors": prettify_author, "page_count": page_count})

        #print(f"\nTitle: {title}")
        #print(f"Author: {prettify_author}")
        #print(f"Page Count: {page_count}")




if __name__ == "__main__":
    app.run(port=5000, debug=True)