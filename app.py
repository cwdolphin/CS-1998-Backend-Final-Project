import json
from flask import Flask, request
from db import db
import dao

app = Flask(__name__)
db_filename = "library.db"

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

@app.route("/api/user/", methods = ['GET'])
def get_all_user():
    a = dao.get_all_user()
    if a is None:
        return failure_response("There are no users.")
    return success_response(a)

@app.route("/api/register/", methods = ['POST'])
def create_user():
    body = json.loads(request.data)
    username = body.get("username","")
    password = body.get("password","")
    if username == "" or password == "":
        return failure_response("Please provide a username and a password")
    u = dao.create_user(username, password)
    if u is None:
        return failure_response("Username already exists")
    return success_response(u)

@app.route("/api/author/", methods = ['POST'])
def create_author():
    body = json.loads(request.data)
    name = body.get("name","")
    if name == "":
        return failure_response("Please provide a name")
    return success_response(dao.create_author(name))

@app.route("/api/book/<int:id>/review/", methods = ['POST'])
def create_review(id):
    body = json.loads(request.data)
    content = body.get("content","")
    username = body.get("username","")
    password = body.get("password","")
    if content == None:
        return failure_response("Please provide a review and a book id!")
    if dao.get_user(username, password) is None:
        return failure_response("Please provide a valid login")
    new_review = dao.create_review(content, id, username, password)
    if new_review is None:
        return failure_response("Either book id or content is invalid")
    return success_response(new_review)

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

@app.route("/api/genre/<int:id>/book/", methods = ['POST'])
def create_book_with_genre(id):
    body = json.loads(request.data)
    new_book = dao.add_book(body.get("title"), body.get("published_year"), id)
    if new_book == None:
        return failure_response("Please provide a valid genre id")
    return success_response(new_book)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)