from db import db, Book, Author, Review, association_table, Genre, User

def get_book(book_id):
  book = Book.query.filter_by(id=book_id).first()
  if book is None:
    return None
  return book.serialize_book()

def add_book(book_title, book_published_year, book_genre_id):
  genre = Genre.query.filter_by(id=book_genre_id).first()
  if genre is None:
    return None
  new_book = Book(title = book_title, published_year = book_published_year, genre_id = book_genre_id)
  db.session.add(new_book)
  db.session.commit()
  return new_book.serialize_book_short()

def delete_book(book_id):
  delete_book = Book.query.filter_by(id=book_id).first()
  if delete_book is None:
      return None
  db.session.delete(delete_book)
  db.session.commit()
  return delete_book.serialize_book_short()

def get_all_books():
  return [b.serialize_book() for b in Book.query.all()]

def create_author(author_name):
  new_author = Author(name = author_name)
  db.session.add(new_author)
  db.session.commit()
  return new_author.serialize_author()

def get_author(author_id):
  author = Author.query.filter_by(id=author_id).first()
  if author is None:
    return None
  return author.serialize_author()

def update_book_with_new_author(author_id, book_id):
  author = Author.query.filter_by(id=author_id).first()
  book = Book.query.filter_by(id=book_id).first()
  if author is None or book is None:
    return None
  book.authors.append(author)
  db.session.commit()
  return book.serialize_book()

def get_all_authors():
  return [a.serialize_author() for a in Author.query.all()]

def create_review(review_text, review_book_id, username, password):
  book = Book.query.filter_by(id=review_book_id).first()
  u = get_user(username, password)
  if book is None or u is None:
    return None
  new_review = Review(content = review_text, book_id = review_book_id, user_id = u.get_id())
  db.session.add(new_review)
  db.session.commit()
  return new_review.serialize_review()

def create_user(username, password):
  user = User.query.filter_by(username=username).first()
  if user is None:
    new_user = User(username = username, password = password)
    db.session.add(new_user)
    db.session.commit()
    return new_user.serialize_user()
  return None

def get_user(username, password):
  user = User.query.filter_by(username=username, password = password).first()
  return user

def get_all_user():
  return [a.serialize_user() for a in User.query.all()]

def get_all_reviews():
  return [a.serialize_review_all() for a in Review.query.all()]

def create_genre(g_name):
  new_genre = Genre(name=g_name)
  db.session.add(new_genre)
  db.session.commit()
  return new_genre.serialize_genre()

def update_book_with_genre(genre_id, book_id):
  genre = Genre.query.filter_by(id=genre_id).first()
  book = Book.query.filter_by(id=book_id).first()
  if genre is None:
    return None
  genre.books.append(book)
  db.session.commit()
  return genre.serialize_genre()

def get_genre(genre_id):
  genre = Genre.query.filter_by(id=genre_id).first()
  if genre is None:
    return None
  return genre.serialize_genre()

def get_all_genre():
  return [g.serialize_genre() for g in Genre.query.all()]