import json
from urllib.request import urlopen
from flask import Flask, flash, jsonify, redirect, render_template, request

app = Flask(__name__)
app.secret_key = "sprigatito906"


@app.route("/add_to_catalogue/title", methods=["GET", "POST"])
def add_book_title():
  title = request.form["title"]
  API = ("https://www.googleapis.com/books/v1/volumes?q=intitle:"+title)
  # response = requests.get(API)
  try:
    with urlopen(API) as response:
      book_data = json.load(response)
      volume_info = book_data["items"][0]["volumeInfo"]
      title = volume_info.get("title", "No Title Available")
      authors = volume_info.get("authors", ["Unknown Author"]) # Sometimes the author is not visible due the URL
                                                               # relying on an older version of Google Books. You can
                                                               # edit the JSON yourself to show it, but that's not
                                                               # the same as extracting the data form the source. This 
                                                               # is the same principle as the dashboard.
      prettify_author = ", ".join(authors)
      page_count = volume_info.get("pageCount", 0)
      thumbnail = volume_info.get("imageLinks", {})["smallThumbnail"]
      
      new_book = {
        "title": title,
        "authors": prettify_author,
        "page_count": page_count,
        "smallThumbnail": thumbnail,
        }
      try:
        with open("catalogue.json", "r+") as catalogue_file:
          catalogue_list = json.load(catalogue_file)
          catalogue_list.append(books)
          catalogue_file.seek(0) # Move cursor to the beginning of the file
          json.dump(catalogue_list, catalogue_file)
        return redirect("/title")
      except FileNotFoundError:
        with open("catalogue.json", "w") as catalogue_file:
          json.dump([books], catalogue_file)
        return redirect("/catalogue_dashboard")
    except (IndexError, KeyError):
      flash("No results found for title")
      return redirect("/catalogue_dashboard")

@app.route("/title")
def catalogue_list():
  return render_template("add_by_title.html")

@app.route("/title/books")
def title_choose():
  try:
    with open("catalogue.json", "r") as catalogue_file:
      catalogue_list = json.load(catalogue_file)
    return jsonify(book_list)
  except FileNotFoundError:
    return jsonify([])

@app.route('/choose_book/<int:title_choose>', methods=["POST"])
def choose_book_clear_list(title_choose):
  try:
    with open("catalogue.json", "r+") as catalogue_file:
      catalogue_list = json.load(catalogue_file)
        if 0 <= title_choose < len(catalogue_list):
          def transfer_to_booklist():
            with open ("catalogue.json", "r") as f:
              source_data = json.load(f)
            with open ("booklist.json", "w") as f:
              json.dump(source_data,f)
          del catalogue_list[title_choose]
          catalogue_file.truncate() # Clear the file
          json.dump(catalogue_list, catalogue_file)
    return redirect('/catalogue_dashboard')
  except FileNotFoundError:
    flash("Catalogue list not found")
    return redirect('/catalogue_dashboard')
