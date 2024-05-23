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
    return render_template("catalogue_dashboard.html")

# To render the template, it has to be done separately from the main function, and the function should be made an
# extension of the template render function.

@app.route("/catalogue_dashboard/books")
def catalogue_books():
    try:
        with open("booklist.json", "r") as book_file:
            book_list = json.load(book_file)
        return jsonify(book_list)
    except FileNotFoundError:
        return jsonify([])

@app.route('/delete_book/<int:catalogue_books>', methods=["POST"])
def delete_book(catalogue_books):
    try:
        with open("booklist.json", "r+") as book_file:
            book_list = json.load(book_file)
            if 0 <= catalogue_books < len(book_list):
                del book_list[catalogue_books] # The function in the brackets will be affected by the delete function
                book_file.seek(0)  # Move cursor to the beginning of the file
                book_file.truncate()  # Clear the file
                json.dump(book_list, book_file)
        return redirect('/catalogue_dashboard')
    except FileNotFoundError:
        flash("Book list not found")
        return redirect('/catalogue_dashboard')

# The delete function is similar to the adding function, which is based on the function in the task list assignment done
# previously. The only difference being the "truncate" function, which will clear the file of the corresponding data
# selected in the table. An analogy of this is using the "Find and Replace" function in a word processor program (e.g.,
# Microsoft Word, Google Docs, etc.) and then detecting the specific word you wish to remove and then delete by
# replacing the word with a blank.

@app.route("/add_to_catalogue")
def add_book():
    return render_template("add_book.html")

@app.route("/add_to_catalogue/isbn", methods=["POST"])
def add_book_isbn():
    ISBN = request.form["ISBN"]
    API = ("https://www.googleapis.com/books/v1/volumes?q=isbn:"+ISBN)

    try:
       with urlopen(API) as response:
        book_data = json.load(response)
        volume_info = book_data["items"][0]["volumeInfo"]
        title = volume_info.get("title", "No Title Available")
        authors = volume_info.get("authors", ["Unknown Author"])  # Sometimes the author is not visible due the URL
                                                                  # relying on an older version of Google Books. You can
                                                                  # edit the JSON yourself to show it, but that's not
                                                                  # the same as extracting the data form the source.
        one_or_multiple_author = ", ".join(authors)
        page_count = volume_info.get("pageCount", 0)
        thumbnail = volume_info.get("imageLinks", {})["smallThumbnail"]

        new_book = {
            "title": title,
            "authors": one_or_multiple_author,
            "page_count": page_count,
            "smallThumbnail": thumbnail,
            }

        try:
            with open("booklist.json", "r+") as book_file:
                book_list = json.load(book_file)
                book_list.append(new_book)
                book_file.seek(0)  # Move cursor to the beginning of the file
                json.dump(book_list, book_file)
            return redirect("/catalogue_dashboard")
        except FileNotFoundError:
            with open("booklist.json", "w") as book_file:
                json.dump([new_book], book_file)
            return redirect("/catalogue_dashboard")
    except (IndexError, KeyError):
        flash("No results found for ISBN")
        return redirect("/catalogue_dashboard")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
