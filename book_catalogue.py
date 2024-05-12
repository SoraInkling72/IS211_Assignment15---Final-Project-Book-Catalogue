import json
from urllib.request import urlopen
from flask import Flask, flash, jsonify, redirect, render_template, request

app = Flask(__name__)
app.secret_key = "sprigatito906"


@app.route("/")
def index():
    return render_template("user_login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # Basic validation
    if username == "student" and password == "bookworm":
        return redirect("/catalogue_dashboard")
    else:
        flash("Please input correct credentials")
        return redirect("/")


@app.route("/catalogue_dashboard")
def catalogue():
    try:
        with open("booklist.json", "r") as book_file:
            book_list = json.load(book_file)
        return jsonify(book_list)
    except FileNotFoundError:
        return jsonify([])


@app.route("/add_to_catalogue", methods=["POST"])
def add_book():
    ISBN = request.form["ISBN"]
    API = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + ISBN
    response = urlopen(API)
    book_data = json.load(response)

    try:
        volume_info = book_data["items"][0]["volumeInfo"]
        title = volume_info.get("title", "No Title Available")
        authors = volume_info.get("authors", ["Unknown Author"])
        prettify_author = ", ".join(authors)
        page_count = volume_info.get("pageCount", 0)

        new_book = {
            "title": title,
            "authors": prettify_author,
            "page_count": page_count,
        }

        try:
            with open("booklist.json", "r+") as book_file:
                book_list = json.load(book_file)
                book_list.append(new_book)
                book_file.seek(0)  # Move cursor to the beginning of the file
                json.dump(book_list, book_file)
        except FileNotFoundError:
            with open("booklist.json", "w") as book_file:
                json.dump([new_book], book_file)

        return redirect("/catalogue_dashboard")
    except (IndexError, KeyError):
        flash("No results found for ISBN")
        return redirect("/catalogue_dashboard")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
