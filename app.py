import json
from flask import Flask, request
from db import db
import dao

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

@app.route("/api/book/<int:id>/", methods = ['GET'])
def get_book(id):
    book = dao.get_book(int(id))
    if book is None:
        return failure_response("There is no book with this id")
    return success_response(book)

@app.route("/api/book/<int:id>/", methods = ['DELETE'])
def del_book(id):
    book = dao.delete_book(id)
    if book is None:
        return failure_response("There is no book with this id")
    return success_response(book)

@app.route("/api/genre/<int:id>/", methods = ['GET'])
def get_genre(id):
    genre = dao.get_genre(int(id))
    if genre is None:
        return failure_response("There is no genre with this id")
    return success_response(genre)

@app.route("/api/author/<int:id>/", methods = ['GET'])
def get_author(id):
    author = dao.get_author(int(id))
    if author is None:
        return failure_response("There is no author with this id")
    return success_response(author)

@app.route("/api/book/", methods = ['GET'])
def get_all_books():
    a = dao.get_all_books()
    if a is None:
        return failure_response("There are no books.")
    return success_response(a)

@app.route("/api/author/", methods = ['GET'])
def get_all_authors():
    a = dao.get_all_authors()
    if a is None:
        return failure_response("There are no authors.")
    return success_response(a)

@app.route("/api/review/", methods = ['GET'])
def get_all_reviews():
    a = dao.get_all_reviews()
    if a is None:
        return failure_response("There are no reviews.")
    return success_response(a)

@app.route("/api/genre/", methods = ['GET'])
def get_all_genre():
    a = dao.get_all_genre()
    if a is None:
        return failure_response("There are no genres.")
    return success_response(a)

@app.route("/api/book/", methods = ['POST'])
def create_book():
    body = json.loads(request.data)
    title = body.get("title","")
    published_year = body.get("year", -1)
    if title == "" or published_year == -1:
        return failure_response("Please provide a title and a published year")
    return success_response(dao.add_book(title, published_year))

@app.route("/api/author/", methods = ['POST'])
def create_author():
    body = json.loads(request.data)
    name = body.get("name","")
    if name == "":
        return failure_response("Please provide a name")
    return success_response(dao.create_author(name))

@app.route("/api/review/", methods = ['POST'])
def create_review():
    body = json.loads(request.data)
    review = body.get("review","")
    book_id = body.get("id","")
    if review == "" or book_id == "":
        return failure_response("Please provide a review and a book id")
    return success_response(dao.create_review(review, book_id))

@app.route("/api/genre/", methods = ['POST'])
def create_genre():
    body = json.loads(request.data)
    name = body.get("name","")
    if name == "":
        return failure_response("Please provide a name for the genre")
    return success_response(dao.create_genre(name))

@app.route("/api/book/<int:id>/author/", methods = ['POST'])
def update_book_author(id):
    body = json.loads(request.data)
    author_id = body.get("author_id", "")
    if author_id == "":
        return failure_response("Please provide a valid author id")
    update = dao.update_book_with_new_author(author_id, id)
    if update is None:
        return failure_response("Either book id or author id is invalid")
    return success_response(update)

@app.route("/api/book/<int:id>/genre/", methods = ['POST'])
def update_book_genre(id):
    body = json.loads(request.data)
    genre_id = body.get("genre_id", "")
    if genre_id == "":
        return failure_response("Please provide a valid genre id")
    update = dao.update_book_with_genre(genre_id, id)
    if update is None:
        return failure_response("Either book id or genre id is invalid")
    return success_response(update)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)